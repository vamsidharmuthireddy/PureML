package impl

import (
	"fmt"

	"github.com/PriyavKaneria/PureML/service/models"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func NewMSQLDatastore() *MySQLDatastore {
	db, err := gorm.Open(mysql.Open(""), &gorm.Config{}) //TODO
	if err != nil {
		fmt.Println(err)
		panic("Error connecting to database")
	}
	return &MySQLDatastore{
		DB: db,
	}
}

type MySQLDatastore struct {
	DB *gorm.DB
}

func (ds *MySQLDatastore) GetAllAdminOrgs() ([]models.Organization, error) {
	//TODO Interact with DB via GORM
	return []models.Organization{}, nil
}
