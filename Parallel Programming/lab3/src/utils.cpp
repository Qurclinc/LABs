#include "utils.hpp"

matrix generateMatrix(int size) {
    srand(time(0));
    int a = 10, b = 100;
    matrix result = matrix(size, std::vector<int>(size, 0));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            result[i][j] = rand() % (b - a + 1);
        }
    }
    return result;
}

void printMatrix(const matrix &M) {
    for (auto vec: M) {
        for (auto elem: vec) {
            std::cout << elem << "  ";
        }
        std::cout << "\n";
    }
}