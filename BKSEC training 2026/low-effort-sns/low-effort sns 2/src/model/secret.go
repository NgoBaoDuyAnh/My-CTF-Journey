package model

type Secret struct {
	Owner  string `json:"owner"`
	Secret string `json:"secret"`
}
