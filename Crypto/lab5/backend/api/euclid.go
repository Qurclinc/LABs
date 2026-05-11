package api

import (
	"math"
	"sort"

	mapset "github.com/deckarep/golang-set/v2"
	"github.com/gin-gonic/gin"
)

type eeaData struct {
	A int64
	B int64
}

type geaData struct {
	List []int
}

func HandleFindEEA(c *gin.Context) {
	var postData eeaData

	if err := c.BindJSON(&postData); err != nil {
		return
	}

	res := findEEA(postData.A, postData.B)
	c.JSON(200, res)
}

func HandleFindGEA(c *gin.Context) {
	var postData geaData

	if err := c.BindJSON(&postData); err != nil {
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

func findGEA(list []int) [][]int {
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
	return result
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
