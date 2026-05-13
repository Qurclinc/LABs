package primality

import (
	"context"
	"math/big"
)

func wilsonWorker(ctx context.Context, n big.Int) bool {
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	one := big.NewInt(1)
	subN := new(big.Int).Sub(&n, one)
	factorial := big.NewInt(1)
	for i := big.NewInt(1); i.Cmp(&n) < 0; i.Add(i, one) {
		select {
		case <-ctx.Done():
			return false
		default:
		}
		factorial.Mul(factorial, i)
		factorial.Mod(factorial, &n)
	}
	if factorial.Cmp(subN) == 0 {
		return true
	}
	return false
}
