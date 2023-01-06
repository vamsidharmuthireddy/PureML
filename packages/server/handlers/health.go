package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

// HealthCheck godoc
// @Summary Show the status of server.
// @Description Get the status of server.
// @Tags root
// @Accept */*
// @Produce json
// @Success 200 {object} map[string]interface{}
// @Router /health [get]
func Health(context echo.Context) error {
	return context.JSON(http.StatusOK, map[string]interface{}{
		"status": 200,
		"data": "Server is up and running🚀🎉",
		"message": "Congratulations!",
	})
}
