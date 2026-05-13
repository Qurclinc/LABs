package primality

import (
	"crypto-lab5/api"
	"math/big"
)

func rabinMillerWorker(n big.Int, limit int64) bool {
	var pickedValues = make(map[string]struct{})
	var k int64
	var a big.Int

	one := big.NewInt(1)
	two := big.NewInt(2)
	subN := new(big.Int).Sub(&n, one)
	s, t := api.DecomposeOfTwo(subN)
outer:
	for k = 0; k < limit; k++ {
		for {
			a = *api.RandBigInt(two, new(big.Int).Sub(&n, two))
			_, existsing := pickedValues[a.String()]
			if !existsing {
				pickedValues[a.String()] = struct{}{}
				break
			}
		}

		gcd := new(big.Int).GCD(nil, nil, &n, &a)
		if gcd.Cmp(one) != 0 {
			return false
		}

		exp := new(big.Int).Exp(&a, &t, &n)
		if exp.Cmp(one) == 0 || exp.Cmp(subN) == 0 { // Надо смотреть второе условие - ибо иначе оно бы потерялось
			continue outer
		}

		limit := new(big.Int).Sub(&s, one)
		for i := big.NewInt(0); i.Cmp(limit) < 0; i.Add(i, one) {

			exp.Exp(exp, two, &n)
			if exp.Cmp(subN) == 0 {
				continue outer
			}
		}
		return false
	}

	return true
}
