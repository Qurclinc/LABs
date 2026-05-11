package primality

import (
	"math/big"

	"github.com/gin-gonic/gin"
)

type primalityData struct {
	N big.Int
}

type chanceData struct {
	N big.Int
	K int64
}

func HandleDevision(c *gin.Context) {
	var data primalityData
	if err := c.BindJSON(&data); err != nil {
		return
	}

	res := runDevisionWorkers(data.N)
	c.JSON(200, res)
}

func HandleShtrassen(c *gin.Context) {
	var data chanceData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	res := strassenWorker(data.N, data.K)
	c.JSON(200, res)
}

func HandleRabinMiller(c *gin.Context) {
	var data chanceData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	res := rabinMillerWorker(data.N, data.K)
	c.JSON(200, res)
}
