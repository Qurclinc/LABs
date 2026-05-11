package primality

import "math/big"

func isPerfectPower(n *big.Int) bool {
	N := new(big.Int).Set(n)
	maxB := big.NewInt(int64(N.BitLen()))
	one := big.NewInt(1)

	for b := big.NewInt(2); b.Cmp(maxB) < 0; b.Add(b, one) {

		// value.Exp(&value, b, nil)
		// if value.Cmp(N) == 0 {
		// 	return true
		// }
	}
	return false
}
