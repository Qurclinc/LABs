#pragma once
#include "HeapSort.h"
#include "Arrays.h"

template <class T>
int interpolationSearch(std::vector<T>& arr, T x, int lo = 0, int hi = -1) {
    if (!isSorted(arr)) {
        throw "Array must be sorted";
    }
    if (hi == -1) {
        hi = arr.size() - 1;
    }
    int pos;
    if (lo <= hi && x >= arr[lo] && x <= arr[hi]) {
        pos = lo + (((double)(hi - lo) / (arr[hi] - arr[lo])) * (x - arr[lo]));

        if (arr[pos] == x) {
            return pos;
        }
        if (arr[pos] <= x) {
            return interpolationSearch(arr, x, pos + 1, hi);
        }
        if (arr[pos] >= x) {
            return interpolationSearch(arr, x, lo, pos - 1);
        }
    }
    return -1;
}

