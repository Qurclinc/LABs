#include "functions.hpp"

int getRandomNumber(int a, int b) {
    if (a >= b) {
        throw std::runtime_error("Invalid range: a < b!");
    }
    int rand_number = rand() % (b - a + 1) + a;
    return rand_number;
}

std::vector<std::vector<int>> generateMatrix(int n, int m) {
    if (n <= 0 || m < 0) {
        throw std::runtime_error("Matrix size must be positive");
    }
    if (m == 0) {
        m = n;
    }


    // Delete this
    // std::vector<std::vector<int>> vec{{21,43,20},{38,19,49},{10,13,33}};
    // return vec;

    std::vector<std::vector<int>> matrix(m, std::vector<int>(n, 0));

    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < m; j++) {
            matrix[i][j] = getRandomNumber(10, 50);
        }
    }
    return matrix;
}

bool isLocalMinimum(const std::vector<std::vector<int>> &matrix, int i, int j) {
    int m = matrix.size();
    for (int x = std::max(i - 1, 0); x <= std::min(m - 1, i + 1); x++) {
        int n = matrix[i].size();
        for (int y = std::max(j - 1, 0); y <= std::min(n - 1, j + 1); y++) {
            if (x == i && y == j) {
                continue;
            }
            if (matrix[i][j] > matrix[x][y]) {
                return false;
            }
        }
    }

    return true;
}

std::vector<int> findLocalMinimums(const std::vector<std::vector<int>> &matrix) {
    auto minimums = std::vector<int>(0);
    for(int i = 0; i < matrix.size(); i++) {
        for(int j = 0; j < matrix[i].size(); j++) {
            if (isLocalMinimum(matrix, i, j)) {
                minimums.push_back(matrix[i][j]);
            }
        }
    }
    return minimums;
}
