package middleware

import (
	"low-effort-sns-2/authentication"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

type AuthenticationMiddleware struct {
	JWKS *authentication.AuthenticationHandler
}

func NewAuthenticationMiddleware(jwks *authentication.AuthenticationHandler) *AuthenticationMiddleware {
	return &AuthenticationMiddleware{
		JWKS: jwks,
	}
}

func (h *AuthenticationMiddleware) VerifyJWT() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		token := ExtractToken(ctx)
		data, err := authentication.VerifyToken(token, h.JWKS.PublicKey)
		if err != nil {
			ctx.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
				"msg":          "invalid key",
				"msg_detailed": err.Error(),
			})
			return
		}
		ctx.Set("uid", data["sub"])
		ctx.Set("role", data["role"])
		ctx.Next()
	}
}

func ExtractToken(c *gin.Context) string {
	authHeader := c.GetHeader("Authorization")
	if data := strings.Split(authHeader, " "); len(data) == 2 {
		return data[1]
	}
	return ""
}
