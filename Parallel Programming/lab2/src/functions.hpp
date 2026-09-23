#include <cstdlib>
#include <ctime>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <math.h>
#include <cstdarg>
#include <algorithm>
#include <chrono>

int getRandomNumber(int a, int b);
std::vector<std::vector<int>> generateMatrix(int n, int m = 0);
bool isLocalMinimum(const std::vector<std::vector<int>> &matrix, int i, int j);
std::vector<int> findLocalMinimums(
    const std::vector<std::vector<int>> &matrix,
    int startX=0, int startY=0,
    int stopX=0, int stopY=0
);

double countTime(std::vector<std::vector<int>> &matrix);

void countParams(
    double T1, double Tn, int p = 1
);

template <typename T>
std::vector<T> mergeVectors(const std::vector<std::vector<T>> &vectors, bool doSort = false) {
    auto result = std::vector<int>();

    for (std::vector<T> vec: vectors) {
        result.insert(result.end(), vec.begin(), vec.end());
    }

    if (doSort) {
        std::sort(result.begin(), result.end());
    }
    return result;
}

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
