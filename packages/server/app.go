package main

import (
	_ "github.com/PriyavKaneria/PureML/service/docs"
	"github.com/PriyavKaneria/PureML/service/handlers"
	"github.com/PriyavKaneria/PureML/service/middlewares"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	echoSwagger "github.com/swaggo/echo-swagger"
)

// @title PureML API Documentation
// @version 1.0

// @contact.name API Support
// @contact.url http://www.swagger.io/support
// @contact.email contact@pureml.com

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host localhost:8080
// @BasePath /
// @schemes http
func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	// e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	//Health API
	e.GET("/health", handlers.Health)
	//Swagger API
	e.GET("/swagger/*", echoSwagger.WrapHandler)

	//Org APIs
	group := e.Group("/org")
	group.GET("/all", handlers.GetAllAdminOrgs, middlewares.AuthenticateJWT)

	//Project APIs
	// group := e.Group("")

	//User APIs
	// group = e.Group("user")

	e.Logger.Fatal(e.Start(":8080"))

}
