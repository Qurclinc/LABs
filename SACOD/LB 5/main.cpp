#include <ctime>
#include <iostream>
#include "Tests.h"

#include <vector>

int main() {
    srand(time(0));
    int lengths[] {10, 20, 50, 100};
    for (int len: lengths) {
        std::cout << "Array's len is: " << len << "\n\n";
        doTest(len);
    }
    return 0;
}