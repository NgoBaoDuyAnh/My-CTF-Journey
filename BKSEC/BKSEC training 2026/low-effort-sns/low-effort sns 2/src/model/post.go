package model

type Post struct {
	Name      string `json:"name"`
	Content   string `json:"content"`
	IsPrivate string `json:"is_private"`
	Owner     string `json:"owner"`
}

type CreatePostReq struct {
	Name      string `json:"name"`
	Content   string `json:"content"`
	IsPrivate string `json:"is_private"` // need convert to true or something here
}

type PostResp struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Content string `json:"content"`
	Owner   string `json:"owner"`
}
