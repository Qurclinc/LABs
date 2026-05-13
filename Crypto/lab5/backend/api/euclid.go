package api

import (
	"math"
	"math/big"
	"sort"

	mapset "github.com/deckarep/golang-set/v2"
	"github.com/gin-gonic/gin"
)

type eeaData struct {
	A string
	B string
}

type geaData struct {
	List []int
}

func HandleFindEEA(c *gin.Context) {
	var postData eeaData

	if err := c.BindJSON(&postData); err != nil {
		return
	}

	a, _ := new(big.Int).SetString(postData.A, 10)
	b, _ := new(big.Int).SetString(postData.B, 10)

	res := findEEABig(a, b)
	c.JSON(200, res)
}

func HandleFindGEA(c *gin.Context) {
	var postData geaData

	if err := c.BindJSON(&postData); err != nil {
		c.JSON(400, gin.H{"error": "invalid json"})
		return
	}

	if len(postData.List) == 0 {
		c.JSON(400, gin.H{"error": "empty list"})
		return
	}

	res := findGEA(postData.List)
	c.JSON(200, res)
}

func findEEA(a int64, b int64) [][]int64 {
	A := math.Abs(float64(a))
	B := math.Abs(float64(b))

	result := [][]int64{
		{int64(math.Max(A, B)), 1, 0},
		{int64(math.Min(A, B)), 0, 1, int64(math.Max(A, B) / math.Min(A, B))},
	}

	i := len(result) - 1
	for {
		a := result[i-1][0] - result[i][0]*result[i][3]
		if a == 0 {
			break
		}
		x := result[i-1][1] - result[i][1]*result[i][3]
		y := result[i-1][2] - result[i][2]*result[i][3]
		q := result[i][0] / a
		line := []int64{a, x, y, q}
		i += 1
		result = append(result, line)
	}

	result = append(result, []int64{0})

	return result
}

func findEEABig(A, B *big.Int) [][]string {
	a := new(big.Int).Set(A)
	b := new(big.Int).Set(B)
	zero := big.NewInt(0)

	var max, min big.Int
	if a.Cmp(b) > 0 {
		max, min = *a, *b
	} else {
		max, min = *b, *a
	}

	result := [][]string{
		{max.String(), "1", "0"},
		{min.String(), "0", "1", new(big.Int).Div(&max, &min).String()},
	}

	i := len(result) - 1
	for {
		res_i_0, _ := new(big.Int).SetString(result[i][0], 10)
		res_i_3, _ := new(big.Int).SetString(result[i][3], 10)
		res_i_s1_0, _ := new(big.Int).SetString(result[i-1][0], 10)
		mulA := new(big.Int).Mul(res_i_0, res_i_3)
		a := new(big.Int).Sub(res_i_s1_0, mulA)
		if a.Cmp(zero) == 0 {
			break
		}

		res_i_s1_1, _ := new(big.Int).SetString(result[i-1][1], 10)
		res_i_1, _ := new(big.Int).SetString(result[i][1], 10)
		mulX := new(big.Int).Mul(res_i_1, res_i_3)
		x := new(big.Int).Sub(res_i_s1_1, mulX)

		res_i_s1_2, _ := new(big.Int).SetString(result[i-1][2], 10)
		res_i_2, _ := new(big.Int).SetString(result[i][2], 10)
		mulY := new(big.Int).Mul(res_i_2, res_i_3)
		y := new(big.Int).Sub(res_i_s1_2, mulY)

		q := new(big.Int).Div(res_i_0, a)

		line := []string{a.String(), x.String(), y.String(), q.String()}
		i++

		result = append(result, line)
	}

	return result
}

func findGEA(list []int) int {
	if len(list) == 0 {
		return -1
	}

	sort.Ints(list)
	result := [][]int{
		list,
	}
	numbers := mapset.NewSet(result[0]...).ToSlice()
	for {
		if len(numbers) == 1 {
			break
		}

		num := findMin(numbers)
		tmp := mapset.NewSet[int]()
		for _, x := range numbers {
			if x == num {
				tmp.Add(x)
			}
			if x == 0 || x%num == 0 {
				continue
			}
			tmp.Add(x % num)
		}
		numbers = tmp.Clone().ToSlice()
		sort.Sort(sort.Reverse(sort.IntSlice(numbers[:])))
		result = append(result, numbers)
	}
	return result[len(result)-1][0]
}

func findMin(numbers []int) int {
	minValue := numbers[0]
	for _, v := range numbers {
		if int(math.Abs(float64(v))) < int(math.Abs(float64(minValue))) {
			minValue = v
		}
	}
	return int(minValue)
}
