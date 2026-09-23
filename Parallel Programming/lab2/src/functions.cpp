#include "functions.hpp"

double countTime(std::vector<std::vector<int>> &matrix) {
    auto start = std::chrono::steady_clock::now();
    findLocalMinimums(matrix);
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double, std::ratio<1>> duration = end - start;
    return duration.count();
}

void countParams(double T1, double Tp, int p) {
    auto S = T1 / Tp;
    auto E = S / p;
    auto C = p * Tp;
    std::cout << "Speed up: " << S << "\nEfficiency: " << E << "\nCost: " << C << "\n\n";
}

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


    // For test only
    // std::vector<std::vector<int>> vec{{10,34,35,14,21},{34,35,21,47,50},{20,37,36,22,24},{37,22,35,19,23},{29,49,36,25,12}};
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

std::vector<int> findLocalMinimums(
    const std::vector<std::vector<int>> &matrix,
    int startX, int startY,
    int stopX, int stopY
) {
    if (startX == 0 && startY == 0 && stopX == 0 && stopY == 0) {
        stopX = matrix[0].size();
        stopY = matrix.size();
    }
    // printf("%d\t%d\t%d\t%d", startX, startY, stopX, stopY);
    auto result = std::vector<int>();
    for(int i = startY; i < stopY; i++) {
        for(int j = startX; j < stopX; j++) {
            if (isLocalMinimum(matrix, i, j)) {
                result.push_back(matrix[i][j]);
            }
        }
    }

    return result;
}
