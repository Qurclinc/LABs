#include "utils.hpp"
#include "serial.hpp"
#include "parallel.hpp"

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
    printf("Matrix generated\nSerial time:\n");
    serialTime(matrix);
    printf("Parallel time:\n");
    parallelTime(matrix);

    // printMatrix(matrix);
    // auto adjency_mat = matrix({
    //     {0, 1, 0, 4},
    //     {1, 0, 1, 0},
    //     {0, 1, 0, 1},
    //     {4, 0, 1, 0}}
    // );

    // serialTime(adjency_mat);
    // parallelTime(adjency_mat);

    return 0;
}