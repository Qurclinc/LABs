#include <stdio.h>

// Составить программу для вычисления суммы факториалов трёх заданных чисел А!+В!+С!

int factorial(int x) {
    int k = 1;
    int fact = 1;
    while (k != x + 1) {
        fact *= k;
        k++;
    }
    return fact;
}

int main() {
    int A = 5, B = 2, C = 7;
    int result = factorial(A) + factorial(B) + factorial(C);
    printf("A! + B! + C! = %d + %d + %d = %d\n", factorial(A), factorial(B), factorial(C), result);
    return 0;
}