#pragma once
#include "Arrays.h"
#include "Sorts.h"
#include <chrono>

// template <class Func>
// void doSort(std::vector<int> &arr, Func sort) {
//     sort(arr);
// }

template <class Func>
double checkTime(std::vector<int> &arr, Func sort) {
    auto start = std::chrono::steady_clock::now();
    sort(arr);
    auto end = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();
}

template <class Func>
void testMiddle(int size, Func sortWrapper) {
    std::vector<int> arr = generateArray(size);
    print(arr);
    std::cout << checkTime(arr, sortWrapper) << "\n";
    print(arr);
}