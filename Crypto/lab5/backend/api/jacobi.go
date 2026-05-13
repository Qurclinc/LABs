package api

import (
	"fmt"
	"math/big"

	"github.com/gin-gonic/gin"
)

type jacobiData struct {
	A string
	N string
}

func HandleJacobiSymbol(c *gin.Context) {
	var data jacobiData
	if err := c.BindJSON(&data); err != nil {
		return
	}

	a, _ := new(big.Int).SetString(data.A, 10)
	n, _ := new(big.Int).SetString(data.N, 10)
	result, err := FindJacobiSymbolBig(a, n)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, result)
}

func findJacobiSymbol(a int64, n int64) int64 {
	a %= n
	var result int64 = 1
	for {
		if a == 0 {
			return 0
		}

		t := 0
		for {
			if a%2 != 0 {
				break
			}
			a /= 2
			t++
		}

		if t%2 != 0 {
			if n%8 == 3 || n%8 == 5 {
				result *= -1
			}
		}

		if a == 1 {
			return result
		}

		if a%4 == 3 && n%4 == 3 {
			result *= -1
		}

		tmp := a
		a = n % a
		n = tmp
	}
}

func FindJacobiSymbolBig(a *big.Int, n *big.Int) (int64, error) {
	A := new(big.Int).Set(a)
	N := new(big.Int).Set(n)
	var mod big.Int
	A.Mod(A, N)
	var result int64 = 1
	zero := big.NewInt(0)
	one := big.NewInt(1)
	two := big.NewInt(2)
	three := big.NewInt(3)
	four := big.NewInt(4)
	five := big.NewInt(5)
	eight := big.NewInt(8)

	if N.Cmp(zero) <= 0 {
		return 0, fmt.Errorf("n должно быть положительным")
	}

	// n нечётное
	if new(big.Int).Mod(N, two).Cmp(zero) == 0 {
		return 0, fmt.Errorf("n должно быть нечётным")
	}

	for {
		if A.Cmp(zero) == 0 {
			return 0, nil
		}
		t := 0
		for {
			if mod.Mod(A, two).Cmp(zero) != 0 {
				break
			}
			A.Div(A, two)
			t++
		}

		if t%2 != 0 {
			nMod8 := new(big.Int).Mod(N, eight)
			if nMod8.Cmp(three) == 0 || nMod8.Cmp(five) == 0 {
				result *= -1
			}
		}

		if A.Cmp(one) == 0 {
			return result, nil
		}

		if new(big.Int).Mod(A, four).Cmp(three) == 0 && new(big.Int).Mod(N, four).Cmp(three) == 0 {
			result *= -1
		}

		tmp := new(big.Int).Set(A)
		A.Mod(N, A)
		N.Set(tmp)
	}
}
