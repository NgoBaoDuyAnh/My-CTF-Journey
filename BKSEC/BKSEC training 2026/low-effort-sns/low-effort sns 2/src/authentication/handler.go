package authentication

import (
	"crypto/rand"
	"crypto/rsa"
	"log"

	"github.com/lestrrat-go/jwx/v3/jwk"
)

type AuthenticationHandler struct {
	KeySet     jwk.Set
	PublicKey  *rsa.PublicKey
	PrivateKey *rsa.PrivateKey
}

func NewAuthHandler() *AuthenticationHandler {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		log.Fatalln("failed to create privkey:", err)
	}

	key, err := jwk.Import(privateKey)
	if err != nil {
		log.Fatalln("failed to create jwks:", err)
	}

	if err := key.Set(jwk.KeyIDKey, "bksec-c307002e-823a-474b-94e3-c89252fb6b44"); err != nil {
		log.Fatalln("failed to add key id")
	}
	if err := key.Set(jwk.AlgorithmKey, "RS256"); err != nil {
		log.Fatalln("failed to add algorithm")
	}

	keySet := jwk.NewSet()
	keySet.AddKey(key)

	return &AuthenticationHandler{
		KeySet:     keySet,
		PublicKey:  &privateKey.PublicKey,
		PrivateKey: privateKey,
	}
}
