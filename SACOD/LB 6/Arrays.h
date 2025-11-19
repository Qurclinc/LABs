#pragma once
#include <cstdio>
#include <cstdlib>
#include <vector>

std::vector<int> generateArray(int len) {
    std::vector<int> arr;
    int start = -200, end = 200;
    for (int i = 0; i < len; i++) {
        arr.push_back(rand() % (end - start + 1) + start);
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

template <class T>
bool isSorted(std::vector<T> &arr) {
    for (int i = 0; i < arr.size() - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}