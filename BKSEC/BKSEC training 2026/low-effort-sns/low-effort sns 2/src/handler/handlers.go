package handler

import (
	"database/sql"
	"low-effort-sns-2/authentication"
	"low-effort-sns-2/middleware"
	"net/http"

	"github.com/gin-gonic/gin"
)

func SetupRoutes(router *gin.Engine, db *sql.DB, jwks *authentication.AuthenticationHandler) {
	loginHandler := NewLoginHandler(db, jwks)
	signUpHandler := NewSignUpHandler(db, jwks)
	profileHandler := NewProfileHandler(db)
	postHandler := NewPostHandler(db)
	secretHandler := NewSecretHandler(db)

	authMiddleware := middleware.NewAuthenticationMiddleware(jwks)

	router.GET("/.well-known/jwks.json", func(c *gin.Context) {
		c.JSON(http.StatusOK, jwks.KeySet)
	})

	router.GET("/", IndexHandler)
	router.GET("/ping", PingHandler)
	router.POST("/login", loginHandler.Login)
	router.POST("/signup", signUpHandler.Signup)

	protected := router.Group("/")
	protected.Use(authMiddleware.VerifyJWT())
	protected.GET("/protected", TestProtectedRoute)
	protected.GET("/profile", profileHandler.ViewOwnProfile)
	protected.GET("/profile/:id", profileHandler.ViewOtherProfile)
	protected.POST("/profile", profileHandler.UpdateProfile)
	protected.GET("/posts", postHandler.GetAllPost)
	protected.GET("/post/:id", postHandler.GetOnePost)
	protected.POST("/posts", postHandler.CreatePost)
	protected.GET("/secret", secretHandler.ViewOwnSecret)

	adminOnly := router.Group("/")
	adminOnly.Use(authMiddleware.VerifyJWT())
	adminOnly.Use(middleware.AdminOnlyMiddleware())
	adminOnly.GET("/secret/:id", secretHandler.ViewOneSecret)
}
