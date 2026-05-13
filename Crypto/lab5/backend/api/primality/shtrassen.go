package primality

import (
	"crypto-lab5/api"
	"math/big"
)

func strassenWorker(n big.Int, limit int64) bool {
	pickedValues := make(map[string]struct{})
	one := big.NewInt(1)
	two := big.NewInt(2)
	var k int64
	var a big.Int
	for k = 0; k < limit; k++ {
		// Уникальное a в диапазоне [2, n-2]
		for {
			a = *api.RandBigInt(two, new(big.Int).Sub(&n, two))
			_, existsing := pickedValues[a.String()]
			if !existsing {
				pickedValues[a.String()] = struct{}{}
				break
			}
		}

		// fmt.Printf("Раунд %d, a = %s\n", k, a.String())

		gcd := new(big.Int).GCD(nil, nil, &a, &n)
		// fmt.Printf("НОД(a, n) = %s\n", gcd.String())
		if gcd.Cmp(one) != 0 {
			// fmt.Printf("НОД > 1 => составное\n")
			return false
		}

		exp := new(big.Int).Sub(&n, one)
		exp.Div(exp, two)
		res := new(big.Int).Exp(&a, exp, &n)
		jacobi, _ := api.FindJacobiSymbolBig(&a, &n)
		var expected big.Int
		expected.Mod(big.NewInt(jacobi), &n)

		// fmt.Printf("exp = %s\n", exp.String())
		// fmt.Printf("res = a^exp mod n = %s\n", res.String())
		// fmt.Printf("Символ Якоби (a/n) = %d\n", jacobi)
		// fmt.Printf("expected (Якоби mod n) = %s\n", expected.String())

		if res.Cmp(&expected) != 0 {
			// fmt.Printf("res != expected => составное\n")
			return false
		}
		// fmt.Printf("res == expected => продолжаем\n\n")
	}
	return true
}
