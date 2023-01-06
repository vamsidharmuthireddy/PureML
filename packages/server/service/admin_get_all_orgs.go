package service

import (
	"fmt"
	"github.com/PriyavKaneria/PureML/service/config"
	"github.com/PriyavKaneria/PureML/service/datastore"
	"github.com/PriyavKaneria/PureML/service/models"
	"net/http"
)

func GetAllAdminOrgs(request *models.Request) *models.Response {
	response := &models.Response{}
	if config.HasAdminAccess(request.UserName) {
		allOrgs, err := datastore.GetAllAdminOrgs()
		if err != nil {
			fmt.Println(err)
			response.Error = err
			response.StatusCode = http.StatusInternalServerError
			response.Body = "Internal server error"
		} else {
			response.StatusCode = http.StatusOK
			response.Body = allOrgs
		}
	} else {
		response.StatusCode = http.StatusForbidden
		response.Body = "Forbidden"
	}
	return response
}
