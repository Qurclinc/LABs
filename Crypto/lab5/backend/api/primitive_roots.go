package api

import (
	"fmt"
	"math/big"

	"github.com/gin-gonic/gin"
)

type primitiveRootData struct {
	N          string
	OnlySingle bool
}

func HandlePrimitiveRoot(c *gin.Context) {
	var data primitiveRootData

	if err := c.BindJSON(&data); err != nil {
		return
	}

	n, _ := new(big.Int).SetString(data.N, 10)
	res, err := findPrimitiveRootsBig(n, data.OnlySingle)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, res)
}

func findPrimitiveRootsBig(n *big.Int, onlySingle bool) ([]string, error) {
	one := big.NewInt(1)
	if n.Cmp(one) <= 0 {
		return nil, fmt.Errorf("n должно быть больше 1")
	}
	if !IsPrime(*n, 10) {
		return nil, fmt.Errorf("n не является простым числом")
	}

	phi := new(big.Int).Sub(n, one)
	var factors []big.Int
	PrimeFactors(*phi, &factors)
	result := make([]string, 0)
	for g := big.NewInt(1); g.Cmp(n) < 0; g.Add(g, one) {
		if new(big.Int).GCD(nil, nil, g, n).Cmp(one) != 0 {
			continue
		}
		is_primitive := true
		for _, prime := range factors {
			if new(big.Int).Exp(g, new(big.Int).Div(phi, &prime), n).Cmp(one) == 0 {
				is_primitive = false
				break
			}
		}
		if is_primitive {
			result = append(result, g.String())
			if onlySingle {
				break
			}
		}
	}

	return result, nil
}
