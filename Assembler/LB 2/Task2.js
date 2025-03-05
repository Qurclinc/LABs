// Даны три числа. Найти произведение наименьшего и наибольшего числа. 

const a = 10
const b = 20
const c = 30

let min, max

if (a >= b && a >= c) {
    max = a
} else if (b >= a && b >= c) {
    max = b
} else if (c >= a && c >= b) {
    max = c
}

if (a <= b && a <= c) {
    min = a
} else if (b <= a && b <= c) {
    min = b
} else if (c <= a && c <= b) {
    min = c
}

const mult = max * min

console.log(mult)