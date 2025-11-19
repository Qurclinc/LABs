#pragma once
#include "CountInt.h"
#include "Arrays.h"
#include "Sorts.h"

void doCount() {
    CountInt::count();
    CountInt::reset();
}

template <class T>
void checkHairbrushSort(std::vector<T> arr) {
    hairbrushSort(arr);
    doCount();
}

template <class T>
void checkStroogeSort(std::vector<T> arr) {
    stoogeSort(arr);
    doCount();
}

void doTest(int size) {
    auto sortedArray = generateSortedArray(size);
    auto unsorderArray = generateArray(size);
    auto reversedSortedArray = generateReversedSortedArray(size);
    std::vector<std::vector<CountInt>> arrays {sortedArray, unsorderArray, reversedSortedArray};
    for (auto arr: arrays) {
        auto copy = arr;
        std::cout << "Hairbrush sort:\n";
        checkHairbrushSort(copy);
        std::cout << "\n";
        std::cout << "Stooge sort:\n";
        checkStroogeSort(copy);
        std::cout << "\n\n\n";
    }

}

