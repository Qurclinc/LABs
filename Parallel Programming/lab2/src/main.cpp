#include "sections.hpp"
#include "for.hpp"
#include <iostream>

int main() {
    srand(time(0));

    int N = -1;
    while (N <= 0) {
        std::cout << "N = ";
        std::cin >> N;
        if (N <= 0) {
            std::cout << "N > 0!\n";
        }
    }

    auto matrix = generateMatrix(N);
    // printMatrix(matrix);
    // printVector(findLocalMinimums(matrix));
    findLocalMinimums(matrix);
    auto T1 = countTime(matrix);

    twoSections(matrix, T1);
    threeSections(matrix, T1);
    fourSections(matrix, T1);

    auto result = findLocalMinimumsParallel(matrix, T1);
    // printVector(result);
    return 0;
}