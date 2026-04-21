package handler

import (
	"database/sql"
	"log"
	"low-effort-sns-2/authentication"
	"low-effort-sns-2/model"
	"low-effort-sns-2/util"
	"net/http"

	"github.com/gin-gonic/gin"
)

type SignUpHandler struct {
	DB          *sql.DB
	JWKSHandler *authentication.AuthenticationHandler
}

func NewSignUpHandler(db *sql.DB, jwks *authentication.AuthenticationHandler) *SignUpHandler {
	return &SignUpHandler{
		DB:          db,
		JWKSHandler: jwks,
	}
}

// @BasePath /

// @Summary Register new account
// @Description Allows a user to register a new account.
// @Tags Authentication
// @Accept json
// @Produce json
// @Param signupData body model.User true "User registration details"
// @Success 201 {object} map[string]string "User successfully registered"
// @Failure 400 {object} map[string]string "Invalid request or missing fields"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /signup [post]
func (h *SignUpHandler) Signup(c *gin.Context) {
	var signupData model.User

	if err := c.BindJSON(&signupData); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "invalid json sent",
		})
		log.Println("error occured during read login JSON:", err)
		return
	}

	if signupData.Username == "" || signupData.Password == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "username and password can not be left blank",
		})
		return
	}

	if signupData.Fullname == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "full name must be supplied",
		})
		return
	}

	insertUser := `INSERT INTO user (username, password, fullname, bio, secret, role) VALUES (?, ?, ?, ?, ?, ?)`

	_, err := h.DB.Exec(insertUser, signupData.Username, util.HashPassword(signupData.Password), signupData.Fullname, signupData.Biography, signupData.Secret, signupData.Role)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}
	log.Println("added user", signupData.Username)
}
