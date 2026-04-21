package handler

import (
	"database/sql"
	"fmt"
	"log"
	"low-effort-sns-2/model"
	"low-effort-sns-2/util"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

type ProfileHandler struct {
	DB *sql.DB
}

type UpdateProfileData struct {
	NewPassword  string `json:"new_password"`
	NewFullname  string `json:"new_full_name"`
	NewBiography string `json:"new_bio"`
	NewSecret    string `json:"new_secret"`
}

func NewProfileHandler(db *sql.DB) *ProfileHandler {
	return &ProfileHandler{
		DB: db,
	}
}

func (h *ProfileHandler) GetProfile(id string) (*model.ProfileResp, error) {
	var user model.ProfileResp
	sqlQuery := `select username, fullname, bio, role from user where id = ?`
	rows, err := h.DB.Query(sqlQuery, id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		err := rows.Scan(&user.Username, &user.Fullname, &user.Biography, &user.Role)
		if err != nil {
			return nil, err
		}
	}
	err = rows.Err()
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// @BasePath /

// ViewOwnProfile retrieves the profile of the authenticated user.
//
// @Summary View own profile
// @Description Fetches the profile details of the currently logged-in user.
// @Tags Profile
// @Produce json
// @Success 200 {object} model.ProfileResp "User profile details"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /profile [get]
func (h *ProfileHandler) ViewOwnProfile(c *gin.Context) {
	uid, exist := c.Get("uid")
	if !exist {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": "your uid has not been set, which should not happen.",
		})
		return
	}
	uidStr, ok := uid.(string)
	if !ok {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": "failed to assert uid is string",
		})
	}

	requestedProfile, err := h.GetProfile(uidStr)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
	}

	if requestedProfile == nil {
		log.Println("nil detected")
		return
	}
	c.JSON(http.StatusOK, requestedProfile)
}

// ViewOtherProfile retrieves the profile of another user by ID.
//
// @Summary View another user's profile
// @Description Fetches the profile details of a specific user based on the provided ID.
// @Tags Profile
// @Produce json
// @Param id path string true "User ID"
// @Success 200 {object} model.ProfileResp "User profile details"
// @Failure 404 {object} map[string]string "User does not exist"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /profile/{id} [get]
func (h *ProfileHandler) ViewOtherProfile(c *gin.Context) {
	id := c.Param("id")
	requestedProfile, err := h.GetProfile(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg":          InternalSerErr,
			"msg_detailed": err.Error(),
		})
		return
	}

	if requestedProfile == nil || *requestedProfile == (model.ProfileResp{}) {
		c.JSON(http.StatusNotFound, gin.H{
			"msg": "user does not exist",
		})
		return
	}
	c.JSON(http.StatusOK, requestedProfile)
}

// UpdateProfile allows an authenticated user to update their profile information.
//
// @Summary Update profile
// @Description Updates the profile of the authenticated user. Fields that can be updated include password, full name, bio, and secret.
// @Tags Profile
// @Accept json
// @Produce json
// @Param updatedProfileReq body UpdateProfileData true "Updated profile fields"
// @Success 200 {object} map[string]string "Profile updated successfully"
// @Failure 400 {object} map[string]string "No fields provided for update or invalid request"
// @Failure 500 {object} map[string]string "Internal server error"
// @Router /profile [put]
func (h *ProfileHandler) UpdateProfile(c *gin.Context) {
	var updatedProfileReq UpdateProfileData
	uid := c.GetString("uid")

	if err := c.BindJSON(&updatedProfileReq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "invalid json received",
		})
	}

	// Prepare dynamic SQL update query
	var fields []string
	var args []interface{}

	if updatedProfileReq.NewPassword != "" {
		fields = append(fields, "password = ?")
		args = append(args, util.HashPassword(updatedProfileReq.NewPassword))
	}
	if updatedProfileReq.NewFullname != "" {
		fields = append(fields, "fullname = ?")
		args = append(args, updatedProfileReq.NewFullname)
	}
	if updatedProfileReq.NewBiography != "" {
		fields = append(fields, "bio = ?")
		args = append(args, updatedProfileReq.NewBiography)
	}
	if updatedProfileReq.NewSecret != "" {
		fields = append(fields, "secret = ?")
		args = append(args, updatedProfileReq.NewSecret)
	}

	if len(fields) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "No fields provided for update"})
		return
	}

	query := fmt.Sprintf("UPDATE user SET %s WHERE id = ?", strings.Join(fields, ", "))
	args = append(args, uid)

	result, err := h.DB.Exec(query, args...)
	if err != nil {
		log.Println("Error updating user:", err)
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "Failed to update profile"})
		return
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		c.JSON(http.StatusNotFound, gin.H{"msg": "User not found - this should not happen."})
		return
	}

	c.JSON(http.StatusOK, gin.H{"msg": "Profile updated successfully"})
}
