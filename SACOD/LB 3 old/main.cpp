#include "LongArithmetic.h"
#include <vector>

void count(std::vector<LongArithmetic> &seq, int N);

int main() {
    int N;
    do {
        std::cout << "Enter N: ";
        std::cin >> N;
    } while (N <= 0);
    std::vector<LongArithmetic> seq = { "1", "1", "1" };
    if (seq.size() < N) {
        count(seq, N);
    }

    // for (auto s : seq) {
    //     std::cout << s.get() << " ";
    // }
    std::cout << seq[N - 1].get() << "\n";
    return 0;
}

void count(std::vector<LongArithmetic> &seq, int N) {
  while (seq.size() != N) {
    seq.push_back(seq[seq.size() - 3] + seq[seq.size() - 2] + seq[seq.size() - 1]);
  }
}