package main

import (
	"crypto-lab5/api"
	"crypto-lab5/api/primality"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.POST("/api/eea", api.HandleFindEEA)
	router.POST("/api/gea", api.HandleFindGEA)

	router.POST("/api/binpow", api.HandleBinPow)
	router.POST("/api/crtpow", api.HandleCrtPow)

	router.POST("/api/inverse", api.HandleInverse)

	router.POST("/api/comparision/single", api.HandleSingleComparision)
	router.POST("/api/comparision/system", api.HandleSystemComparision)
	router.POST("/api/comparision/square", api.HandleSquareComparision)

	router.POST("/api/jacobi", api.HandleJacobiSymbol)

	router.POST("/api/devision", primality.HandleDevision)
	router.POST("/api/wilson", primality.HandleWilson)
	router.POST("/api/lucas", primality.HandleLucas)

	router.POST("/api/ferm", primality.HandleFerm)
	router.POST("/api/strassen", primality.HandleShtrassen)
	router.POST("/api/rabin", primality.HandleRabinMiller)

	router.Run("0.0.0.0:8000")
}
