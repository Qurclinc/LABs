package api

import (
	"fmt"
	"math/big"

	"github.com/fxtlabs/primes"
	"github.com/gin-gonic/gin"
)

type inverseData struct {
	A        string
	M        string
	ForceEEA bool
}

func HandleInverse(c *gin.Context) {
	var data inverseData

	if err := c.BindJSON(&data); err != nil {
		return
	}
	a, _ := new(big.Int).SetString(data.A, 10)
	m, _ := new(big.Int).SetString(data.M, 10)

	result, err := findMultiplicativeInverseBig(a, m)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, result)
}

func findMultiplicativeInverse(a int64, m int64, forceEEA bool) (int64, error) {
	var err error

	if m <= 0 {
		return -1, fmt.Errorf("Модуль должен быть положительным")
	}

	a %= m
	res := findEEA(a, m)
	gcd := res[len(res)-2][0]
	if gcd != 1 {
		return -1, fmt.Errorf("НОД(%d, %d) != 1", a, m)
	}
	var result int64
	if forceEEA {
		result = res[len(res)-2][1]
	} else {
		if primes.IsPrime(int(m)) {
			result, err = binaryPow(a, m-2, m)
			if err != nil {
				return -1, err
			}
		} else {
			result = res[len(res)-2][1]
		}
	}

	return result, nil
}

func findMultiplicativeInverseBig(A, M *big.Int) (string, error) {
	a := new(big.Int).Set(A)
	m := new(big.Int).Set(M)
	res := findEEABig(a, m)
	gcd, _ := new(big.Int).SetString(res[len(res)-1][0], 10)

	if gcd.Cmp(big.NewInt(1)) != 0 {
		return "-1", fmt.Errorf("НОД(%s, %s) != 1", a.String(), m.String())
	}

	inv, _ := new(big.Int).SetString(res[len(res)-1][2], 10)
	result := inv.Mod(inv, m)
	return result.String(), nil
}
