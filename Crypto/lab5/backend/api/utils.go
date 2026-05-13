package api

import (
	"fmt"
	"math/big"
	"math/rand"
	"time"
)

var source = rand.New(rand.NewSource(time.Now().UTC().UnixNano()))

func Unpack(src []int64, dst ...*int64) {
	for i, value := range dst {
		*value = src[i]
	}
}

func RandBigInt(min *big.Int, max *big.Int) *big.Int {
	return big.NewInt(0).Add(min, big.NewInt(0).Rand(source, big.NewInt(0).Add(big.NewInt(0).Sub(max, min), big.NewInt(1))))
}

func ArePairwiseCoprime(coeffs [][]string) bool {

	for i := 0; i < len(coeffs); i++ {
		m1, _ := new(big.Int).SetString(coeffs[i][2], 10)

		for j := i + 1; j < len(coeffs); j++ {
			m2, _ := new(big.Int).SetString(coeffs[j][2], 10)

			line := findEEABig(m1, m2)
			gcd := line[len(line)-1][0]
			if gcd != "1" {
				return false
			}
		}
	}
	return true
}

func PrimeFactors(N big.Int, factors *[]big.Int) {
	n := new(big.Int).Set(&N)
	zero := big.NewInt(0)
	one := big.NewInt(1)
	two := big.NewInt(2)
	if new(big.Int).Mod(n, two).Cmp(zero) == 0 {
		*factors = append(*factors, *big.NewInt(2))
	}
	for {
		if new(big.Int).Mod(n, two).Cmp(zero) != 0 {
			break
		}
		n.Div(n, two)
	}

	var limit big.Int
	for i := big.NewInt(3); i.Cmp(limit.Sqrt(n).Add(&limit, one)) <= 0; i.Add(i, two) {
		if new(big.Int).Mod(n, i).Cmp(zero) == 0 {
			*factors = append(*factors, *new(big.Int).Set(i))
		}
		for {
			if new(big.Int).Mod(n, i).Cmp(zero) != 0 {
				break
			}
			n.Div(n, i)
		}
	}

	if n.Cmp(two) == 1 {
		*factors = append(*factors, *n)
	}
}

func PrimePowers(n *big.Int) []*big.Int {
	result := []*big.Int{}
	tmp := new(big.Int).Set(n)
	i := big.NewInt(2)

	for tmp.Cmp(big.NewInt(1)) > 0 {
		count := 0
		for new(big.Int).Mod(tmp, i).Cmp(big.NewInt(0)) == 0 {
			tmp.Div(tmp, i)
			count++
		}

		if count > 0 {
			pow := new(big.Int).Exp(i, big.NewInt(int64(count)), nil)
			result = append(result, pow)
		}

		i.Add(i, big.NewInt(1))
	}

	return result
}

func DecomposeOfTwo(n *big.Int) (big.Int, big.Int) {
	N := new(big.Int).Set(n)
	zero := big.NewInt(0)
	one := big.NewInt(1)
	two := big.NewInt(2)
	var s big.Int
	for {
		if new(big.Int).Mod(N, two).Cmp(zero) != 0 {
			break
		}
		N.Div(N, two)
		s.Add(&s, one)
	}
	return s, *N
}

func FindM(B, P *big.Int) *big.Int {
	one := big.NewInt(1)
	two := big.NewInt(2)

	b := new(big.Int).Set(B)
	p := new(big.Int).Set(P)
	m := big.NewInt(1)

	for {
		exp := new(big.Int).Exp(two, m, nil)
		res := new(big.Int).Exp(b, exp, p)
		if res.Cmp(one) == 0 {
			break
		}
		m.Add(m, one)
	}

	return m
}

// ----------- Validations ----------------

func ParsePositiveBigInt(s string) (*big.Int, error) {
	n, ok := new(big.Int).SetString(s, 10)
	if !ok {
		return nil, fmt.Errorf("invalid number")
	}
	if n.Sign() <= 0 {
		return nil, fmt.Errorf("n must be positive")
	}
	return n, nil
}

func ValidateK(k int64) error {
	if k <= 0 {
		return fmt.Errorf("k must be > 0")
	}
	return nil
}
