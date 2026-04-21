package handler

import (
	"database/sql"
	"log"
	"low-effort-sns-2/model"
	"net/http"

	"github.com/gin-gonic/gin"
)

type PostHandler struct {
	DB *sql.DB
}

func NewPostHandler(db *sql.DB) *PostHandler {
	return &PostHandler{
		DB: db,
	}
}

// @BasePath /

// GetAllPost retrieves all public posts.
//
// @Summary Get all public posts
// @Description Retrieves all posts that are not marked as secret.
// @Tags Posts
// @Produce json
// @Success 200 {array} model.PostResp "List of public posts"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /posts [get]
func (h *PostHandler) GetAllPost(c *gin.Context) {
	var posts []model.PostResp

	sqlQuery := `select id, postname, postcontent, user_id from post where is_secret = 0`
	rows, err := h.DB.Query(sqlQuery)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": "error occured during querying",
		})
		return
	}

	for rows.Next() {
		var post model.PostResp
		err := rows.Scan(&post.ID, &post.Name, &post.Content, &post.Owner)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg":          InternalSerErr,
				"msg_detailed": "error occured during scanning",
			})
			return
		}
		posts = append(posts, post)
	}

	err = rows.Err()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, posts)
}

// GetOnePost retrieves a specific post by ID.
//
// @Summary Get a specific post
// @Description Fetches a post by its ID. If the post is private, only the owner can access it.
// @Tags Posts
// @Produce json
// @Param id path string true "Post ID"
// @Success 200 {object} model.PostResp "Post details"
// @Failure 403 {object} map[string]string "Forbidden: Post is private"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /posts/{id} [get]
func (h *PostHandler) GetOnePost(c *gin.Context) {
	var post model.PostResp
	var isSecret bool

	id := c.Param("id")

	sqlQuery := `select id, postname, postcontent, is_secret, user_id from post where id = ?`
	err := h.DB.QueryRow(sqlQuery, id).Scan(&post.ID, &post.Name, &post.Content, &isSecret, &post.Owner)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": "error during querying post",
		})
	}

	if isSecret {
		if c.GetString("uid") != post.Owner {
			c.JSON(http.StatusForbidden, gin.H{
				"msg": "this post is invalid or currently private",
			})
			return
		}
	}

	c.JSON(http.StatusOK, post)
}

// CreatePost allows a user to create a new post.
//
// @Summary Create a new post
// @Description Allows an authenticated user to create a new post. The post can be marked as private or public.
// @Tags Posts
// @Accept json
// @Produce json
// @Param post body model.CreatePostReq true "Post details"
// @Success 200 {object} map[string]interface{} "Post successfully created"
// @Failure 400 {object} map[string]string "Invalid request or missing fields"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /posts [post]
func (h *PostHandler) CreatePost(c *gin.Context) {
	uid := c.GetString("uid")
	var post model.CreatePostReq

	if err := c.BindJSON(&post); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "invalid json received",
		})
		return
	}

	log.Println(post)
	if post.Name == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "post name can not be blank",
		})
		return
	}

	sqlQuery := `insert into post (postname, postcontent, is_secret, user_id) values (?, ?, ?, ?)`
	result, err := h.DB.Exec(sqlQuery, post.Name, post.Content, post.IsPrivate, uid)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}

	if aff, _ := result.RowsAffected(); aff == 0 {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": "post can not be uploaded",
		})
		return
	}

	insertedId, err := result.LastInsertId()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": "can not get last inserted id",
		})
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "post has been published",
		"id":  insertedId,
	})
}
