package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// @BasePath /

// TestProtectedRoute verifies access to a protected route.
//
// @Summary Test protected route
// @Description Returns a welcome message if the user has access to the protected route.
// @Tags Test
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} map[string]string "Welcome message"
// @Router /protected [get]
func TestProtectedRoute(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"msg": "welcome to protected route",
	})
}
