package primality

import (
	"crypto-lab5/api"
	"math/big"
)

func fermWorker(n big.Int, k int64) bool {

	var gcd big.Int
	var powered big.Int
	one := big.NewInt(1)
	two := big.NewInt(2)
	subN := new(big.Int).Sub(&n, one)
	sub2N := new(big.Int).Sub(&n, two)

	for i := int64(0); i < k; i++ {
		a := api.RandBigInt(two, sub2N)
		gcd.GCD(nil, nil, a, &n)
		if gcd.Cmp(one) != 0 {
			return false
		}

		powered.Exp(a, subN, &n)
		if powered.Cmp(one) != 0 {
			return false
		}
	}

	return true
}
