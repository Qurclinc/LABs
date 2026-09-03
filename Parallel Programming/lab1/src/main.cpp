#include "sections.hpp"
#include <iostream>

int main() {
    srand(time(0));
    auto matrix = generateMatrix(10);
    printMatrix(matrix);
    // printVector(findLocalMinimums(matrix));
    twoSections(matrix);
    threeSections(matrix);
    fourSections(matrix);
    return 0;
}