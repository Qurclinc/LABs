#include <stdio.h>

// f(x) = 5x^3 - x^2 + 6 Написать подпрограмму, вычисляющую значение функции 4f(x1) + f(x2)

int f(int x) {
    return 5 * x * x * x - x * x + 6;
}

int main(void) {
    int x1 = 1, x2 = 5;
    int f1 = 4 * f(x1);
    int f2 = f(x2);
    int result = f1 + f2;
    printf("4f(x1) + f(x2) = %d + %d = %d\n", f1, f2, result);
}