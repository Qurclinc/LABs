#pragma once
#include <vector>
#include <cmath>

void hairbrushSort(std::vector<int> &arr) {
    const double factor = 1.247;
    double gapFactor = arr.size() / factor;

    while (gapFactor > 1) {
        int gap = round(gapFactor);
        for (int i = 0, j = gap; j < arr.size(); i++, j++) {
            if (arr[i] > arr[j]) {
                std::swap(arr[i], arr[j]);
            }
        }
        gapFactor /= factor;
    }
}

void stoogeSort(std::vector<int> &arr, int l = 0, int h = -1) {
    if (h == -1) {
        h = arr.size() - 1;
    }
    if (l >= h) {
        return;
    }
    if (arr[l] > arr[h]) {
        std::swap(arr[l], arr[h]);
    }

    if (h - l + 1 > 2) {
        int t = (h - l + 1) / 3;
        stoogeSort(arr, l, h - t);
        stoogeSort(arr, l + t, h);
        stoogeSort(arr, l, h - t);
    }
}

void hairbrushSortWrapper(std::vector<int> &arr) {
    hairbrushSort(arr);
}

void stoogeSortWrapper(std::vector<int> &arr) {
    stoogeSort(arr);
}