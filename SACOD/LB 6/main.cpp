#include <iostream>
#include "HeapSort.h"
#include "InterpolationSearch.h"
#include "Arrays.h"
#include <cmath>

int main() {
    int N = 10;
    std::vector<int> arr = generateArray(N);
    print(arr);
    heapSort(arr);
    std::cout << "Sorted array: ";
    print(arr);
    if (arr.size() >= 2) {
        int minDiff = arr[1] - arr[0];
        int elem1 = arr[0], elem2 = arr[1];
        for (int i = 1; i < arr.size() - 1; i++) {
            if (arr[i + 1] - arr[i] < minDiff) {
                minDiff = arr[i + 1] - arr[i];
                elem1 = arr[i];
                elem2 = arr[i + 1];
            }
        }
        std::cout << "Minimal difference is between " << elem1 << " and " << elem2 << "\n";
    } else {
        std::cout << "There's less than 2 elements in array\n";
    }




    // int N;
    // std::cout << "Enter element: ";
    // std::cin >> N;
    // std::cout << "Its index is: " << interpolationSearch(arr, N);
    return 0;
}