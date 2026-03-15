package handler

import (
	"database/sql"
	"low-effort-sns-2/authentication"
	"low-effort-sns-2/util"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v4"
)

type LoginHandler struct {
	DB          *sql.DB
	JWKSHandler *authentication.AuthenticationHandler
}

func NewLoginHandler(db *sql.DB, jwks *authentication.AuthenticationHandler) *LoginHandler {
	return &LoginHandler{
		DB:          db,
		JWKSHandler: jwks,
	}
}

type LoginData struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// @BasePath /

// @Summary Authenticate user
// @Description Authenticates a user using their username and password. If the credentials are correct, a JWT token is returned.
// @Tags Authentication
// @Accept json
// @Produce json
// @Param loginData body LoginData true "Username and Password"
// @Success 200 {object} map[string]interface{} "Successful login"
// @Failure 400 {object} map[string]string "Invalid request or missing fields"
// @Failure 403 {object} map[string]string "Invalid username or password"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /login [post]
func (h *LoginHandler) Login(c *gin.Context) {
	var loginData LoginData

	if err := c.BindJSON(&loginData); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "received invalid json",
		})
		return
	}

	if loginData.Username == "" || loginData.Password == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "username and password can not be left blank",
		})
		return
	}

	var id, hashedPw, role string
	queryUser := `SELECT id, password, role FROM user where username = ?`
	rows, err := h.DB.Query(queryUser, loginData.Username)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}
	defer rows.Close()

	for rows.Next() {
		err := rows.Scan(&id, &hashedPw, &role)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg":          InternalSerErr,
				"msg_detailed": err.Error(),
			})
			return
		}
	}
	err = rows.Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}

	err = util.CheckPassword(loginData.Password, hashedPw)
	if err != nil {
		c.JSON(http.StatusForbidden, gin.H{
			"msg": "username or password is wrong",
		})
		return
	}

	token := jwt.NewWithClaims(jwt.SigningMethodRS256, jwt.MapClaims{
		"sub":      id,
		"username": loginData.Username,
		"role":     role,
		"exp":      time.Now().Add(time.Minute * 5).Unix(),
		"iat":      time.Now().Unix(),
	})

	token.Header["kid"] = "bksec-c307002e-823a-474b-94e3-c89252fb6b44"

	tokenString, err := token.SignedString(h.JWKSHandler.PrivateKey)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"msg":   "correct credentials, welcome!",
		"token": tokenString,
	})
}
