package primality

import (
	"fmt"
	"math/big"

	"github.com/gin-gonic/gin"
)

type primalityData struct {
	N string
}

type chanceData struct {
	N string
	K int64
}

// ----------- Validations ----------------

func ParsePositiveBigInt(s string) (*big.Int, error) {
	n, ok := new(big.Int).SetString(s, 10)
	if !ok {
		return nil, fmt.Errorf("invalid number")
	}
	if n.Sign() <= 0 {
		return nil, fmt.Errorf("n must be > 0")
	}
	return n, nil
}

func ValidateK(k int64) error {
	if k <= 0 {
		return fmt.Errorf("k must be > 0")
	}
	return nil
}

// ----------- helper ----------------

func bad(c *gin.Context, msg string) {
	c.JSON(400, gin.H{"error": msg})
}

// ----------- handlers ----------------

func HandleDevision(c *gin.Context) {
	var data primalityData
	ctx := c.Request.Context()

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	res := runDevisionWorkers(ctx, *n)
	c.JSON(200, res)
}

func HandleWilson(c *gin.Context) {
	var data primalityData
	ctx := c.Request.Context()

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	res := wilsonWorker(ctx, *n)
	c.JSON(200, res)
}

func HandleLucas(c *gin.Context) {
	var data primalityData
	ctx := c.Request.Context()

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	res := lucasWorker(ctx, *n)
	c.JSON(200, res)
}

func HandleFerm(c *gin.Context) {
	var data chanceData

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	if err := ValidateK(data.K); err != nil {
		bad(c, err.Error())
		return
	}

	res := fermWorker(*n, data.K)
	c.JSON(200, res)
}

func HandleShtrassen(c *gin.Context) {
	var data chanceData

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	if err := ValidateK(data.K); err != nil {
		bad(c, err.Error())
		return
	}

	res := strassenWorker(*n, data.K)
	c.JSON(200, res)
}

func HandleRabinMiller(c *gin.Context) {
	var data chanceData

	if err := c.BindJSON(&data); err != nil {
		bad(c, "invalid json")
		return
	}

	n, err := ParsePositiveBigInt(data.N)
	if err != nil {
		bad(c, err.Error())
		return
	}

	if err := ValidateK(data.K); err != nil {
		bad(c, err.Error())
		return
	}

	res := rabinMillerWorker(*n, data.K)
	c.JSON(200, res)
}
