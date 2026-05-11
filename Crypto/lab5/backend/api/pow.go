package api

import (
	"strconv"

	"github.com/gin-gonic/gin"
)

type powData struct {
	A int64
	N int64
	M int64
}

func HandlePow(c *gin.Context) {
	var data powData

	if err := c.BindJSON(&data); err != nil {
		return
	}

	result := binaryPow(data.A, data.N, data.M)
	c.JSON(200, result)
}

func binaryPow(a int64, n int64, m int64) int64 {
	binaryForm := strconv.FormatInt(n, 2)
	current := a
	for _, bit := range binaryForm[1:] {
		switch bit {
		case '1':
			current = (current * current) % m
			current = (current * a) % m
		case '0':
			current = (current * current) % m
		}
	}

	return current
}
