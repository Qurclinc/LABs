#include "functions.hpp"
#include <omp.h>

void twoSections(const std::vector<std::vector<int>> &matrix, double T1);
void threeSections(const std::vector<std::vector<int>> &matrix, double T1);
void fourSections(const std::vector<std::vector<int>> &matrix, double T1);