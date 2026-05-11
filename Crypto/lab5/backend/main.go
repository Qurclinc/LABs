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
	router.POST("/api/pow", api.HandlePow)
	router.POST("/api/inverse", api.HandleInverse)
	router.POST("/api/comparision/single", api.HandleSingleComparision)
	router.POST("/api/comparision/system", api.HandleSystemComparision)
	router.POST("/api/jacobi", api.HandleJacobiSymbol)
	router.POST("/api/devision", primality.HandleDevision)
	router.POST("/api/strassen", primality.HandleShtrassen)
	router.POST("/api/rabin", primality.HandleRabinMiller)

	router.Run("localhost:8000")
}
