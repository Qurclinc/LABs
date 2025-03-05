#include <iostream>
#include "Integer.h"

Integer getNumber(std::vector<Integer> &seq, int N);

int main() {
    std::vector<Integer> seq {Integer("1"), Integer("1"), Integer("1")};
    int N;
    do {
        std::cout << "Enter N > 0\nN = ";
        std::cin >> N;
    } while (N <= 0);
    std::cout << getNumber(seq, N);
    return 0;
}

Integer getNumber(std::vector<Integer> &seq, int N) {
    int counter = 3;
    if (N <= 3) {
        return Integer("1");
    }
    while (counter != N) {
        seq.push_back(seq[seq.size() - 3] + seq[seq.size() - 2] + seq[seq.size() - 1]);
        counter++;
    }
    return seq[seq.size() - 1];
}