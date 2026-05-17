package primality

import (
	"crypto-lab5/api"
	"math/big"
)

func rabinMillerWorker(n big.Int, limit int64) bool {
	return api.IsPrime(n, limit)
}
