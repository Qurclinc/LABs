package api

import (
	"github.com/fxtlabs/primes"
	"github.com/gin-gonic/gin"
)

type inverseData struct {
	A        int64
	M        int64
	ForceEEA bool
}

func HandleInverse(c *gin.Context) {
	var data inverseData

	if err := c.BindJSON(&data); err != nil {
		return
	}

	result := findMultiplicativeInverse(data.A, data.M, data.ForceEEA)
	c.JSON(200, result)
}

func findMultiplicativeInverse(a int64, m int64, forceEEA bool) int64 {
	res := findEEA(a, m)
	gcd := res[len(res)-2][0]
	if gcd != 1 {
		return -1
	}
	var result int64
	if forceEEA {
		result = res[len(res)-2][1]
	} else {
		if primes.IsPrime(int(m)) {
			result = binaryPow(a, m-2, m)
		} else {
			result = res[len(res)-2][1]
		}
	}

	return result
}
