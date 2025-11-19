#pragma once
#include <cstdio>
#include <cstdlib>
#include <vector>
#include "CountInt.h"

std::vector<CountInt> generateArray(int len) {
    std::vector<CountInt> arr;
    int start = -200, end = 200;
    for (int i = 0; i < len; i++) {
        arr.push_back(CountInt(rand() % (end - start + 1) + start));
    }
    return arr;
}

std::vector<CountInt> generateSortedArray(int len) {
    std::vector<CountInt> arr;
    for (int i = 0; i < len; i++) {
        arr.push_back(CountInt(i));
    }
    return arr;
}

std::vector<CountInt> generateReversedSortedArray(int len) {
    std::vector<CountInt> arr;
    for (int i = len - 1; i >= 0; i--) {
        arr.push_back(CountInt(i));
    }
    return arr;
}


template <class T>
void print(std::vector<T> &arr) {
    for (auto i : arr) {
        std::cout << i << " ";
    }
    printf("\n");
}

