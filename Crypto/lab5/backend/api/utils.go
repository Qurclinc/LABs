package api

import (
	"math/big"
	"math/rand"
	"time"
)

func Unpack(src []int64, dst ...*int64) {
	for i, value := range dst {
		*value = src[i]
	}
}
func RandBigInt(min *big.Int, max *big.Int) *big.Int {
	source := rand.New(rand.NewSource(time.Now().UTC().UnixNano()))
	return big.NewInt(0).Add(min, big.NewInt(0).Rand(source, big.NewInt(0).Add(big.NewInt(0).Sub(max, min), big.NewInt(1))))
}

func NthRoot(n *big.Int, k int64) (root *big.Int, rem *big.Int) {
	var (
		n0    = big.NewInt(0)
		n1    = big.NewInt(1)
		kk    = big.NewInt(k)
		kMin1 = big.NewInt(k - 1)
	)

	if n.Sign() == 0 {
		return big.NewInt(0), big.NewInt(0)
	}
	if k == 1 {
		return new(big.Int).Set(n), n0
	}

	shift := (n.BitLen() + int(k) - 1) / int(k)
	guess := new(big.Int).Lsh(big.NewInt(1), uint(shift))

	var (
		guessPowK_1 = new(big.Int)
		cube        = new(big.Int)
		dx          = new(big.Int)
		absDx       = new(big.Int)
		minDx       = new(big.Int).Abs(n)
		fx          = new(big.Int)
		fxp         = new(big.Int)
		step        = new(big.Int)
	)

	for {
		cube.Exp(guess, kk, nil)
		dx.Sub(n, cube)
		cmp := dx.Cmp(n0)
		if cmp == 0 {
			return guess, n0
		}

		fx.Sub(cube, n)
		guessPowK_1.Exp(guess, kMin1, nil)
		fxp.Mul(kk, guessPowK_1)
		step.Div(fx, fxp)
		if step.Cmp(n0) == 0 {
			step.Set(n1)
		}

		absDx.Abs(dx)
		switch absDx.Cmp(minDx) {
		case -1:
			minDx.Set(absDx)
		case 0:

			if cube.Cmp(n) > 0 {
				guess.Sub(guess, n1)
				cube.Exp(guess, kk, nil)
				dx.Sub(n, cube)
			}
			return guess, dx
		}

		guess.Sub(guess, step)
	}
}
