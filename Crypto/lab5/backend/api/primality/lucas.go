package primality

import (
	"context"
	"crypto-lab5/api"
	"math/big"
)

func lucasWorker(ctx context.Context, n big.Int) bool {

	zero := big.NewInt(0)
	one := big.NewInt(1)
	two := big.NewInt(2)
	subN := new(big.Int).Sub(&n, one)

	if n.Cmp(two) == 0 {
		return true
	}

	if new(big.Int).Mod(&n, two).Cmp(zero) == 0 {
		return false
	}

	var factors []big.Int
	api.PrimeFactors(*subN, &factors)

	size := new(big.Int).Sub(&n, big.NewInt(3))
	var tmp big.Int

	random := make(map[string]string)
	for i := big.NewInt(0); i.Cmp(size) < 0; i.Add(i, one) {
		random[i.String()] = tmp.Add(i, two).String()
	}

	pickedValues := make(map[string]struct{})
	var a big.Int
	var power, exp big.Int

	for i := big.NewInt(2); i.Cmp(new(big.Int).Sub(&n, two)) < 0; i.Add(i, one) {
		for {
			select {
			case <-ctx.Done():
				return false
			default:
			}
			a = *api.RandBigInt(two, new(big.Int).Sub(&n, two))
			_, existsing := pickedValues[a.String()]
			if !existsing {
				pickedValues[a.String()] = struct{}{}
				break
			}
		}
		power.Exp(&a, subN, &n)
		if power.Cmp(one) != 0 {
			return false
		}

		flag := true
		for k := 0; k < len(factors); k++ {
			exp.Div(subN, &factors[k])
			power.Exp(&a, &exp, &n)
			if power.Cmp(one) == 0 {
				flag = false
				break
			}
		}
		if flag {
			return true
		}
	}
	return false
}
