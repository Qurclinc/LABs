package api

import (
	"fmt"
	"math/big"

	"github.com/gin-gonic/gin"
)

type squareCompData struct {
	A string
	B string
	M string
}

func HandleSquareComparision(c *gin.Context) {
	var data squareCompData
	if err := c.BindJSON(&data); err != nil {
		return
	}
	a, _ := new(big.Int).SetString(data.A, 10)
	b, _ := new(big.Int).SetString(data.B, 10)
	m, _ := new(big.Int).SetString(data.M, 10)
	res, err := solveSquareComparision(a, b, m)
	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	c.JSON(200, res)
}

func solveSquareComparision(a, b, m *big.Int) (string, error) {
	one := big.NewInt(1)
	two := big.NewInt(2)

	// Нормализуем если коэффициент при х не 1
	if a.Cmp(one) != 0 {
		invValue, err := findMultiplicativeInverseBig(a, m)
		inv, _ := new(big.Int).SetString(invValue, 10)

		if err != nil {
			return "", err
		}
		a = big.NewInt(1)
		b.Mul(inv, b)
	}
	jacobi, err := FindJacobiSymbolBig(b, m)
	if err != nil {
		return "", err
	}

	// 0 шаг: а вычет ли вообще
	switch jacobi {
	case 1:
	case -1:
		return "Нет решений", nil
	case 0:
		return "0", nil
	}

	// 1 шаг: нужно выбрать такое n чтобы символ Лежандра чтобы он был -1
	var n big.Int
	min := big.NewInt(1)
	max := new(big.Int).Sub(m, one)
	for {
		n = *RandBigInt(min, max)
		jacobi, _ := FindJacobiSymbolBig(&n, m)
		if jacobi == -1 {
			break
		}
	}

	// 2 шаг: нужно найти соотношение m - 1 = 2^e * q
	e, q := DecomposeOfTwo(new(big.Int).Sub(m, one))

	// 3 шаг: сделать предположения/задать переменные
	y := new(big.Int).Exp(&n, &q, m)
	r := new(big.Int).Set(&e)
	exp := new(big.Int).Sub(&q, one)
	exp.Div(exp, two)
	x := new(big.Int).Exp(b, exp, m)

	// 4 шаг: ещё переменные
	B := new(big.Int).Mul(b, new(big.Int).Mul(x, x))
	B.Mod(B, m)
	X := new(big.Int).Mul(b, x)
	X.Mod(X, m)

	// 5 шаг: основной цикл
	for {
		if B.Cmp(one) == 0 {
			break
		}

		// M = m; m = p из методички

		// a)
		M := new(big.Int).Set(FindM(B, m))

		// б)
		topExp := new(big.Int).Sub(r, M)
		topExp.Sub(topExp, one)
		fullExp := new(big.Int).Exp(two, topExp, nil)
		t := new(big.Int).Exp(y, fullExp, m)
		y = new(big.Int).Exp(t, two, m)
		r = new(big.Int).Set(M)

		// в)
		X.Mul(X, t)
		X.Mod(X, m)
		B.Mul(B, y)
		B.Mod(B, m)
	}

	return fmt.Sprintf("x ≡ %s (mod %s); x ≡ %s (mod %s)",
		X.String(), m.String(), new(big.Int).Sub(m, X).String(), m.String(),
	), nil
}
