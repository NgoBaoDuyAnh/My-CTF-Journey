package authentication

import (
	"crypto/rsa"
	"fmt"

	"github.com/golang-jwt/jwt/v4"
)

func VerifyToken(tokenString string, pubKey *rsa.PublicKey) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("got invalid signing method: %s", t.Method.Alg())
		}
		return pubKey, nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return nil, jwt.ErrSignatureInvalid
	}

	if err := claims.Valid(); err != nil {
		return nil, err
	}

	return claims, nil
}
