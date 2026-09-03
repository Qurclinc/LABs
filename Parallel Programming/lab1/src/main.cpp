#include "functions.hpp"
#include <iostream>

int main() {
    srand(time(0));
    auto matrix = generateMatrix(5);
    printMatrix(matrix);
    auto result = findLocalMinimums(matrix);
    std::cout << "\n";
    printVector(result);
    return 0;
}