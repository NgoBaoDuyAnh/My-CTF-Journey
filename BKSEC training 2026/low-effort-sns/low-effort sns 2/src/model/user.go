package model

type User struct {
	Username  string `json:"username"`
	Password  string `json:"password"`
	Fullname  string `json:"full_name"`
	Biography string `json:"bio"`
	Secret    string `json:"secret"`
	Role      string `json:"role"`
}

type ProfileResp struct {
	Username  string `json:"username"`
	Fullname  string `json:"full_name"`
	Biography string `json:"bio"`
	Role      string `json:"role"`
}
