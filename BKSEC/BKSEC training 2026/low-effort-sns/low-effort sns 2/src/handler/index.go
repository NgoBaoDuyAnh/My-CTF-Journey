package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type IndexMsg struct {
	Name           string `json:"name"`
	Version        string `json:"version"`
	Description    string `json:"description"`
	HealthCheckURL string `json:"health_check"`
	Status         string `json:"status"`
}

// @BasePath /

// IndexHandler godoc
// @Summary Index
// @Schemes https
// @Description Index - home page of this service.
// @Tags General Usage
// @Produce json
// @Success 200 {object} map[string]string
// @Router / [get]
func IndexHandler(c *gin.Context) {
	c.JSON(http.StatusOK, IndexMsg{
		Name:           "API-SNS",
		Version:        "1.33.7",
		Description:    "Welcome to API-SNS, a social networking platform designed for developers and automation enthusiasts. Connect, share, and interact through API-driven interactions.",
		HealthCheckURL: "/ping",
		Status:         "🚀🚀 the application is up and running.",
	})
}
