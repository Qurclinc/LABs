#include <iostream>
#include <ctime>
#include <cmath>
#include "Arrays.h"
#include "Sorts.h"
#include "Tests.h"


int main() {
    srand(time(0));
    int lengths[] {10, 20, 50, 100};
    int len = lengths[0];
    testMiddle(len, stoogeSortWrapper);
    // auto arr = generateArray(10);
    // print(arr);
    // // doSort(arr, hairbrushSortWrapper);
    // // doSort(arr, stoogeSortWrapper);
    // print(arr);
    // stoogeSort(arr);
    // print(arr);
    return 0;
}