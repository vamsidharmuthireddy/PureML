package models

type Request struct {
	UserName    string
	Body        []byte
	Headers     map[string]string
	PathParams  map[string]string
	QueryParams map[string]string
}

type Response struct {
	Error      error
	Body       interface{}
	StatusCode int
}

type Organization struct {
	Id           string      `json:"id"`
	Name         string      `json:"name"`
	APITokenHash string      `json:"api_token_hash"`
	JoinCode     string      `json:"join_code"`
	Users        interface{} `json:"users"`
}
