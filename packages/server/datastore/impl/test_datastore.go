package impl

import "github.com/PriyavKaneria/PureML/service/models"

func NewTestDatastore() *TestDatastore {
	return &TestDatastore{}
}

type TestDatastore struct {
}

func (ds *TestDatastore) GetAllAdminOrgs() ([]models.Organization, error) {
	return []models.Organization{}, nil
}
