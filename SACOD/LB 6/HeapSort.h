#pragma once
#include <vector>

template <class T>
void heapify(std::vector<T> &arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest]) {
        largest = l;
    }

    if (r < n && arr[r] > arr[largest]) {
        largest = r;
    }

    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

template <class T>
void buildHeap(std::vector<T> &arr) {
    int start = (arr.size() / 2) - 1;
    for (int i = start; i >= 0; i--) {
        heapify(arr, arr.size(), i);
    }
}

template <class T>
void heapSort(std::vector<T> &arr) {
    buildHeap(arr);
    for (int i = arr.size() - 1; i >= 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
