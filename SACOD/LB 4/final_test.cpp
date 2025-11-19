#include <iostream>
#include <chrono>
#include "QuickPow.h"
#include <cmath>

typedef unsigned long long ull;

int main() {
    ull x = 1, res;
    const int iterations = 10000; // Количество повторений для усреднения

    // Используем steady_clock для замера времени
    for (int k = 1; k < 29; k++) {
        double total_time = 0;
        ull n = std::pow(2, k);
        // Повторяем вычисление несколько раз
        for (int i = 0; i < iterations; i++) {
            auto start = std::chrono::steady_clock::now(); // Начало замера
            res = QuickPow(x, n);
            auto end = std::chrono::steady_clock::now();   // Конец замера

            // Вычисляем продолжительность в наносекундах
            total_time += std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
        }

        // Усредняем время выполнения
        double avg_time = total_time / iterations;

        // std::cout << x << " ^ " << k << " = " << res 
        //           << "\tAverage Time: " << avg_time << " ns\n";
        // std::cout << n << "\n";
        std::cout << avg_time << "\n";
    }

    return 0;
}
