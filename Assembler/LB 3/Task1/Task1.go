package main

// Найти произведение первых n нечетных чисел натурального ряда.

import "fmt"

func main() {
	n := 5
	k := 1
	mult := 1
	for i := 0; ; {
		if i == n {
			break
		}
		if k%2 != 0 {
			mult *= k
			i++
		}
		k++
	}
	fmt.Printf("%d\n", mult)
}
