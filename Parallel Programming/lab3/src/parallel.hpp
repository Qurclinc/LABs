#include "utils.hpp"
#include <chrono>
#include <omp.h>


matrix floydAlgorithmParallel(const matrix &M);
void parallelTime(const matrix &M);