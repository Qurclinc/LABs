#include <vector>
#include <omp.h>


std::vector<int> findLocalMinimumsParallel(
    const std::vector<std::vector<int>> &matrix,
    double T1,
    int startX=0, int startY=0,
    int stopX=0, int stopY=0
);