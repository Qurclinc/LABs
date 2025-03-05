#include <iostream>
#include <ctime>
#include <cstdlib>

#include "Sorts.h"
#include "Testing.h"

std::vector<int> generateArray(int n);
void print(std::vector<int> &arr);

int main() {
    srand(time(0));
    const int N = 10;
    std::vector<int> arr = generateArray(N);
    print(arr);
    // ShakerSort(arr);
    // QuickSort(arr, 0, N - 1);
    // SelectSort(arr);
    // ShellSort(arr, Shell);
    // ShellSort(arr, Knutt);
    // ShellSort(arr, Pratt);
    // ShellSort(arr, Fibbonacchi);
    // HairbrushSort(arr);
    // InsertSort(arr);
    print(arr);
    if (isSorted(arr)) {
        std::cout << "\nArray is sorted\n";
    }
    else {
        std::cout << "\nArray is not sorted\n";
    }
    return 0;
}

std::vector<int> generateArray(int n) {
    std::vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
    }
    return arr;
}

void print(std::vector<int> &arr) {
    for (auto i: arr) {
        std::cout << i << " ";
    }
    std::cout << "\n";
}