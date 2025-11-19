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



void print(std::vector<int> &arr) {
    for (auto i : arr) {
        printf("%d ", i);
    }
    printf("\n");
}

