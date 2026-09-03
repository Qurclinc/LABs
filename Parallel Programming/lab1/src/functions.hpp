#include <cstdlib>
#include <ctime>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <math.h>

int getRandomNumber(int a, int b);
std::vector<std::vector<int>> generateMatrix(int n, int m = 0);
bool isLocalMinimum(const std::vector<std::vector<int>> &matrix, int i, int j);
std::vector<int> findLocalMinimums(const std::vector<std::vector<int>> &matrix);

template <typename T>
void printMatrix(const std::vector<std::vector<T>> &matrix, char delimiter='\t') {
    for (size_t i = 0; i < matrix.size(); i++) {
        for (size_t j = 0; j < matrix[i].size(); j++) {
            std::cout << matrix[i][j] << delimiter;
        }
        std::cout << "\n";
    }
}

template <typename T>
void printVector(const std::vector<T> &vector, char delimiter='\t') {
    for (size_t i = 0; i < vector.size(); i++) {
        std::cout << vector [i] << delimiter;
    }
        std::cout << "\n";
}
