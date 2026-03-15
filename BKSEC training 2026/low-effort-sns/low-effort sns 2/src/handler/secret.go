package handler

import (
	"database/sql"
	"low-effort-sns-2/model"
	"net/http"

	"github.com/gin-gonic/gin"
)

type SecretHandler struct {
	DB *sql.DB
}

func NewSecretHandler(db *sql.DB) *SecretHandler {
	return &SecretHandler{
		DB: db,
	}
}

func (h *SecretHandler) GetSecret(id string) (*model.Secret, error) {
	secretResp := &model.Secret{Owner: id}

	sqlQuery := `select secret from user where id = ?`
	err := h.DB.QueryRow(sqlQuery, id).Scan(&secretResp.Secret)
	if err != nil {
		return nil, err
	}
	return secretResp, nil
}

// @BasePath /

// ViewOwnSecret retrieves the secret of the authenticated user.
//
// @Summary View own secret
// @Description Fetches the secret associated with the currently logged-in user.
// @Tags Secret
// @Produce json
// @Success 200 {object} model.Secret "User's secret"
// @Failure 404 {object} map[string]string "User does not have a secret"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /secret [get]
func (h *SecretHandler) ViewOwnSecret(c *gin.Context) {
	uid := c.GetString("uid")
	secretResponse, err := h.GetSecret(uid)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": InternalSerErr,
		})
		return
	}

	if secretResponse.Secret == "" {
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "user seems to not have a secret",
		})
		return
	}

	c.JSON(http.StatusOK, secretResponse)
}

// ViewOneSecret retrieves the secret of another user by ID.
//
// @Summary View another user's secret
// @Description Fetches the secret associated with a specific user based on the provided ID.
// @Tags Secret
// @Produce json
// @Param id path string true "User ID"
// @Success 200 {object} model.Secret "User's secret"
// @Failure 404 {object} map[string]string "User does not have a secret"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /secret/{id} [get]
func (h *SecretHandler) ViewOneSecret(c *gin.Context) {
	id := c.Param("id")
	secretResponse, err := h.GetSecret(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": InternalSerErr,
		})
		return
	}

	if secretResponse.Secret == "" {
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "user seems to not have a secret",
		})
		return
	}

	c.JSON(http.StatusOK, secretResponse)
}
