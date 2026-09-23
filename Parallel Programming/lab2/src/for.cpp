#include "for.hpp"
#include "functions.hpp"

std::vector<int> findLocalMinimumsParallel(
    const std::vector<std::vector<int>> &matrix,
    double T1,
    int startX, int startY,
    int stopX, int stopY
) {
    if (startX == 0 && startY == 0 && stopX == 0 && stopY == 0) {
        stopX = matrix[0].size();
        stopY = matrix.size();
    }
    // printf("%d\t%d\t%d\t%d", startX, startY, stopX, stopY);
    auto result = std::vector<int>();

    int threads = omp_get_max_threads();
    std::vector<std::vector<int>> localResults(threads);

    double start = omp_get_wtime();
    int threads_num;

    #pragma omp parallel 
    {
        threads_num = omp_get_num_threads();
        int tid = omp_get_thread_num();
        
        #pragma omp for collapse(2)
        for(int i = startY; i < stopY; i++) {
            for(int j = startX; j < stopX; j++) {
                if (isLocalMinimum(matrix, i, j)) {
                    localResults[tid].push_back(matrix[i][j]);
                }
            }
        }
    }

    double end = omp_get_wtime();

    printf("Parallel For: %.6f sec\n", end - start);
    countParams(T1, (end - start), threads_num);

    for (auto &local: localResults) {
        result.insert(result.end(), local.begin(), local.end());
    }

    std::sort(result.begin(), result.end());
    return result;
}