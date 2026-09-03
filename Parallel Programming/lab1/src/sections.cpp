#include "sections.hpp"

void twoSections(const std::vector<std::vector<int>> &matrix) {
    std::vector<int> r1, r2 = std::vector<int>();
    int n = matrix.size();
    int m = matrix[0].size();
    #pragma omp parallel sections 
    {
        #pragma omp section
        {
            r1 = findLocalMinimums(matrix, 0, 0, n / 2, m);
        }
        #pragma omp section
        {
            r2 = findLocalMinimums(matrix, n / 2, 0, n, m);
        }
    }
    auto result = mergeVectors(std::vector<std::vector<int>>{r1, r2}, true);
    printVector(result);
}

void threeSections(const std::vector<std::vector<int>> &matrix) {
    std::vector<int> r1, r2, r3 = std::vector<int>();
    int n = matrix.size();
    int m = matrix[0].size();
    #pragma omp parallel sections 
    {
        #pragma omp section
        {
            r1 = findLocalMinimums(matrix, 0, 0, n, m / 3);
        }
        #pragma omp section
        {
            r2 = findLocalMinimums(matrix, 0, m / 3, n, 2 * m / 3);
        }
        #pragma omp section
        {
            r3 = findLocalMinimums(matrix, 0, 2 * m / 3, n, m);
        }
    }
    auto result = mergeVectors(std::vector<std::vector<int>>{r1, r2, r3}, true);
    printVector(result);
}

void fourSections(const std::vector<std::vector<int>> &matrix) {
    std::vector<int> r1, r2, r3, r4 = std::vector<int>();
    int n = matrix.size();
    int m = matrix[0].size();
    #pragma omp parallel sections 
    {
        #pragma omp section
        {
            r1 = findLocalMinimums(matrix, 0, 0, n / 2, m / 2);
        }
        #pragma omp section
        {
            r2 = findLocalMinimums(matrix, n / 2, 0, n, m / 2);
        }
        #pragma omp section
        {
            r3 = findLocalMinimums(matrix, 0, m / 2, n / 2, m);
        }
        #pragma omp section
        {
            r4 = findLocalMinimums(matrix, n / 2, m / 2, n, m);
        }
    }
    auto result = mergeVectors(std::vector<std::vector<int>>{r1, r2, r3, r4}, true);
    printVector(result);
}
