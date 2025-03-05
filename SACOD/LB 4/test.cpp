#include <iostream>
#include <chrono>
#include "QuickPow.h"

typedef unsigned long long ull;

int main() {
    ull x = 1, res;
    const int iterations = 10000; // Количество повторений для усреднения

    // Используем steady_clock для замера времени
    for (int a = 0; a < 1000; a++) {
        double total_time = 0;

        // Повторяем вычисление несколько раз
        for (int i = 0; i < iterations; ++i) {
            auto start = std::chrono::steady_clock::now(); // Начало замера
            res = QuickPow(x, a);
            auto end = std::chrono::steady_clock::now();   // Конец замера

            // Вычисляем продолжительность в наносекундах
            total_time += std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
        }

        // Усредняем время выполнения
        double avg_time = total_time / iterations;

        // std::cout << x << " ^ " << a << " = " << res 
        //           << "\tAverage Time: " << avg_time << " ns\n";
        std::cout << avg_time << "\n";
    }

    return 0;
}
