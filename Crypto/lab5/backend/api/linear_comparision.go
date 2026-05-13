package api

import (
	"fmt"
	"math/big"

	"github.com/gin-gonic/gin"
)

type singleCompData struct {
	A string
	B string
	M string
}

type systemCompData struct {
	Coeffs [][]string
}

type SystemCompAnswer struct {
	X string
	M string
}

func HandleSingleComparision(c *gin.Context) {
	var data singleCompData
	if err := c.BindJSON(&data); err != nil {
		return
	}

	a, _ := new(big.Int).SetString(data.A, 10)
	b, _ := new(big.Int).SetString(data.B, 10)
	m, _ := new(big.Int).SetString(data.M, 10)

	result := solveSingleComparisionBig(a, b, m)
	c.JSON(200, result)
}

func HandleSystemComparision(c *gin.Context) {
	var data systemCompData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	result, err := solveSystemComparisionsBig(data.Coeffs)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, result)
}

///// LEEEGACY!!
// func solveSingleComparision(a int64, b int64, m int64) int64 {
// 	a %= m
// 	b %= m

// 	line := findEEA(a, m)
// 	res := line[len(line)-2]
// 	d := res[0]
// 	if b%d != 0 {
// 		return -1
// 	}
// 	inv := res[2]
// 	x := (inv * b) % m
// 	return x
// }

// func solveSystemComparisions(coeffs [][]int64) (SystemCompAnswer, error) {
// 	for i, coeff := range coeffs {
// 		if len(coeff) != 3 {
// 			if len(coeff) == 2 {
// 				coeffs[i] = []int64{1, coeff[0], coeff[1]}
// 			} else {
// 				panic("LengthError")
// 			}
// 		}
// 	}

// 	if !ArePairwiseCoprime(coeffs) {
// 		return SystemCompAnswer{}, fmt.Errorf("Модули не являются попарно взаимнопростыми")
// 	}

// 	var a, b, m int64
// 	Unpack(coeffs[0], &a, &b, &m)
// 	x := solveSingleComparision(a, b, m)
// 	M := m
// 	// Отправная точка

// 	for _, coeff := range coeffs[1:] {
// 		Unpack(coeff, &a, &b, &m)
// 		// println(a, "\t", b, "\t", m, "\t", x, "\t", M)
// 		A := (a * M)
// 		B := (b - a*x)

// 		t := solveSingleComparision(A, B, m)
// 		x = x + M*t
// 		M = M * m

// 		x = (x + M) % M // Нормализация по модулю
// 	}

// 	return SystemCompAnswer{X: x, M: M}, nil
// }

func solveSingleComparisionBig(A, B, M *big.Int) string {
	a := new(big.Int).Set(A)
	b := new(big.Int).Set(B)
	m := new(big.Int).Set(M)

	a.Mod(a, m)
	b.Mod(b, m)
	zero := big.NewInt(0)

	line := findEEABig(a, m)
	res := line[len(line)-1]
	d, _ := new(big.Int).SetString(res[0], 10)
	if new(big.Int).Mod(b, d).Cmp(zero) != 0 {
		return "Нет решений"
	}

	inv, _ := new(big.Int).SetString(res[2], 10)
	x := new(big.Int).Mul(inv, b)
	x.Mod(x, m)

	return x.String()
}

func solveSystemComparisionsBig(coeffs [][]string) (SystemCompAnswer, error) {
	for i, coeff := range coeffs {
		if len(coeff) != 3 {
			if len(coeff) == 2 {
				coeffs[i] = []string{"1", coeff[0], coeff[1]}
			} else {
				panic("LengthError")
			}
		}
	}

	if !ArePairwiseCoprime(coeffs) {
		return SystemCompAnswer{}, fmt.Errorf("Модули не являются попарно взаимнопростыми")
	}

	a, _ := new(big.Int).SetString(coeffs[0][0], 10)
	b, _ := new(big.Int).SetString(coeffs[0][1], 10)
	m, _ := new(big.Int).SetString(coeffs[0][2], 10)

	x, _ := new(big.Int).SetString(solveSingleComparisionBig(a, b, m), 10)
	M := m
	// Отправная точка

	for _, coeff := range coeffs[1:] {
		a, _ := new(big.Int).SetString(coeff[0], 10)
		b, _ := new(big.Int).SetString(coeff[1], 10)
		m, _ := new(big.Int).SetString(coeff[2], 10)

		// println(a, "\t", b, "\t", m, "\t", x, "\t", M)
		A := new(big.Int).Mul(a, M)
		mulB := new(big.Int).Mul(a, x)
		B := new(big.Int).Sub(b, mulB)

		t, _ := new(big.Int).SetString(solveSingleComparisionBig(A, B, m), 10)

		mulMt := new(big.Int).Mul(M, t)
		x.Add(x, mulMt)
		M.Mul(M, m)

		x.Mod(x, M) // Нормализация по модулю
	}

	return SystemCompAnswer{X: x.String(), M: M.String()}, nil
}
