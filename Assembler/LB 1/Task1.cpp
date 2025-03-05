#include <iostream>

// Даны два числа. Найти их среднее арифметическое и среднее арифметическое их квадратов. 

int main() {
    int a, b;
    a = 10;
    b = 20;

    int avg = (a + b) / 2;
    int square_avg = (a * a + b * b) / 2;
    std::cout << avg << "\n" << square_avg << "\n";
}