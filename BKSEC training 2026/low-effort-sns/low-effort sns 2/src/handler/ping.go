package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// @BasePath /

// PingHandler godoc
// @Summary HealthCheck
// @Schemes https
// @Description Simple health check endpoint.
// @Tags General Usage
// @Produce json
// @Success 200 {object} map[string]string
// @Router /ping [get]
func PingHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
}
