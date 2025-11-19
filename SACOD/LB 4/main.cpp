#include <iostream>
#include <chrono>
#include "QuickPow.h"
#include <cmath>

typedef unsigned long long ull;

int main() {
    ull x = 1, res;
    const int iterations = 10000;
    for (int k = 1; k < 29; k++) {
        double total_time = 0;
        ull n = std::pow(2, k);
        for (int i = 0; i < iterations; i++) {
            auto start = std::chrono::steady_clock::now(); // Начало замера
            res = QuickPow(x, n);
            auto end = std::chrono::steady_clock::now();   // Конец замера

            // Продолжительность в наносекундах
            total_time += std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
        }
        double avg_time = total_time / iterations;

        std::cout << "n = 2^" << k << "; \tTime: " << avg_time << "\n";
    }

    return 0;
}
