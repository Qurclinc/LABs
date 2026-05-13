package api

import (
	"fmt"
	"math/big"
	"strconv"

	"github.com/gin-gonic/gin"
)

type powData struct {
	A string
	N string
	M string
}

func HandleBinPow(c *gin.Context) {
	var data powData

	if err := c.BindJSON(&data); err != nil {
		return
	}

	a, _ := new(big.Int).SetString(data.A, 10)
	n, _ := new(big.Int).SetString(data.N, 10)
	m, _ := new(big.Int).SetString(data.M, 10)

	result, err := bigBinaryPow(*a, *n, *m)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, result)
}

func HandleCrtPow(c *gin.Context) {
	var data powData

	if err := c.BindJSON(&data); err != nil {
		return
	}

	a, _ := new(big.Int).SetString(data.A, 10)
	n, _ := new(big.Int).SetString(data.N, 10)
	m, _ := new(big.Int).SetString(data.M, 10)

	result, err := crtPow(a, n, m)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, result)
}

func binaryPow(a int64, n int64, m int64) (int64, error) {

	if m <= 0 {
		return 0, fmt.Errorf("модуль должен быть > 0")
	}
	if n < 0 {
		return 0, fmt.Errorf("степень должна быть >= 0")
	}

	if n == 0 {
		return 1 % m, nil
	}

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

	return current, nil
}

func bigBinaryPow(a, n, m big.Int) (string, error) {

	zero := big.NewInt(0)
	if m.Cmp(zero) <= 0 {
		return "", fmt.Errorf("Модуль должен быть > 0")
	}
	if n.Cmp(zero) < 0 {
		return "", fmt.Errorf("Степень должна быть >= 0")
	}

	if n.Cmp(zero) == 0 {
		return new(big.Int).Mod(big.NewInt(1), &m).String(), nil
	}

	binaryForm := fmt.Sprintf("%b", new(big.Int).Set(&n))
	current := new(big.Int).Set(&a)
	for _, bit := range binaryForm[1:] {
		switch bit {
		case '1':
			current.Mul(current, current)
			current.Mod(current, &m)
			current.Mul(current, &a)
			current.Mod(current, &m)

		case '0':
			current.Mul(current, current)
			current.Mod(current, &m)
		}
	}

	return current.String(), nil
}

func crtPow(a, n, m *big.Int) (string, error) {
	modules := PrimePowers(m)
	var coeffs [][]string

	for _, mod := range modules {
		coeff := new(big.Int).Exp(a, n, mod)
		coeffs = append(coeffs, []string{coeff.String(), mod.String()})
	}
	result, err := solveSystemComparisionsBig(coeffs)

	return result.X, err
}
