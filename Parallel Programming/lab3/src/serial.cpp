#include "serial.hpp"

matrix floydAlgorithm(const matrix &M) {
    auto R = M;
    int n = R.size();
    try {
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if ((i == j) || (R[i][k] <= 0) || (R[k][j] <= 0)) continue;
                    if ((R[i][k] + R[k][j] < R[i][j]) || (R[i][j] <= 0)) {
                        R[i][j] = R[i][k] + R[k][j];
                    }
                }
            }
        }
    }
    catch (...) {
        printf("Error");
    }
    return R;
}

void serialTime(const matrix &M) {
    auto start = std::chrono::steady_clock::now();
    floydAlgorithm(M);
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << "Elapsed time: " << elapsed.count() << "ms\n";
}