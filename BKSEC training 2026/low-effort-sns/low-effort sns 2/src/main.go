package main

import (
	"fmt"
	"low-effort-sns-2/authentication"
	"low-effort-sns-2/database"
	"low-effort-sns-2/handler"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	_ "modernc.org/sqlite"

	"low-effort-sns-2/docs"

	swaggerfiles "github.com/swaggo/files"     // swagger embed files
	ginSwagger "github.com/swaggo/gin-swagger" // gin-swagger middleware
)

//	@title			API-SNS
//	@version		1.33.7
//	@description	A social networking platform designed for developers and automation enthusiasts. Connect, share, and interact through API-driven interactions.

//	@host		loweffsns2.bksec.vn
//	@BasePath	/

//	@securityDefinitions.apikey	JWT
//	@in							header
//	@name						Authorization
//	@description				JWT Key for Authorization. Example: Authorization: Bearer XXXX

func main() {
	for _, e := range os.Environ() {
		pair := strings.SplitN(e, "=", 2)
		fmt.Println(pair[0], pair[1])
	}
	db := database.InitDB()
	defer db.Close()

	database.InitAdminAccount(db)

	docs.SwaggerInfo.BasePath = "/"

	jwksHandler := authentication.NewAuthHandler()

	router := gin.Default()
	router.HandleMethodNotAllowed = true
	handler.SetupRoutes(router, db, jwksHandler)
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerfiles.Handler))
	router.Run(":1337")
}
