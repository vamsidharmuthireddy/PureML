package middlewares

import "github.com/labstack/echo/v4"

func AuthenticateJWT(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		//TODO to write the logic here
		return next(c)
	}
}
