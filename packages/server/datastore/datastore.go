package datastore

import (
	"github.com/PriyavKaneria/PureML/service/datastore/impl"
	"github.com/PriyavKaneria/PureML/service/models"
)

var ds Datastore = nil

func init() {
	ds = &impl.TestDatastore{} //TODO to switch with real datastrore
}

func GetAllAdminOrgs() ([]models.Organization, error) {
	return ds.GetAllAdminOrgs()
}

type Datastore interface {
	GetAllAdminOrgs() ([]models.Organization, error)
}
