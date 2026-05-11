package api

import (
	"github.com/gin-gonic/gin"
)

type singleCompData struct {
	A int64
	B int64
	M int64
}

type systemCompData struct {
	Coeffs [][]int64
}

type SystemCompAnswer struct {
	X int64
	M int64
}

func HandleSingleComparision(c *gin.Context) {
	var data singleCompData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	result := solveSingleComparision(data.A, data.B, data.M)
	c.JSON(200, result)
}

func HandleSystemComparision(c *gin.Context) {
	var data systemCompData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	result := solveSystemComparisions(data.Coeffs)
	c.JSON(200, result)
}

func solveSingleComparision(a int64, b int64, m int64) int64 {
	a %= m
	b %= m

	line := findEEA(a, m)
	res := line[len(line)-2]
	d := res[0]
	if b%d != 0 {
		return -1
	}
	inv := res[2]
	x := (inv * b) % m
	return x
}

func solveSystemComparisions(coeffs [][]int64) SystemCompAnswer {
	for i, coeff := range coeffs {
		if len(coeff) != 3 {
			if len(coeff) == 2 {
				coeffs[i] = []int64{1, coeff[0], coeff[1]}
			} else {
				panic("LengthError")
			}
		}
	}

	// Проверить что все модули взаимно простые

	var a, b, m int64
	Unpack(coeffs[0], &a, &b, &m)
	x := solveSingleComparision(a, b, m)
	M := m
	// Отправная точка

	for _, coeff := range coeffs[1:] {
		Unpack(coeff, &a, &b, &m)
		// println(a, "\t", b, "\t", m, "\t", x, "\t", M)
		A := (a * M)
		B := (b - a*x)

		t := solveSingleComparision(A, B, m)
		x = x + M*t
		M = M * m

		x = (x + M) % M // Нормализация по модулю
	}

	return SystemCompAnswer{X: x, M: M}
}
