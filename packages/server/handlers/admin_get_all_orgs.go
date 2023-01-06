package handlers

import (
	"github.com/PriyavKaneria/PureML/service/service"
	"github.com/labstack/echo/v4"
)

// GetAllAdminOrgs godoc
// @Summary Get all organizations and their details.
// @Description Get all organizations and their details. Only accessible by admins.
// @Tags root
// @Accept */*
// @Produce json
// @Success 200 {object} map[string]interface{}
// @Router /org/all [get]
func GetAllAdminOrgs(context echo.Context) error {
	request := extractRequest(context)
	response := service.GetAllAdminOrgs(request)
	var err error
	if response.Error != nil {
		err = response.Error
	} else {
		context.Response().WriteHeader(response.StatusCode)
		responseWriter := context.Response().Writer
		_, err = responseWriter.Write(convertToBytes(response.Body))
	}
	return err
}
