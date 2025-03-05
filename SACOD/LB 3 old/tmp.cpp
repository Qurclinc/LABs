#include <iostream>
#include <string>
#include <vector>

std::string add(std::string n1, std::string n2);
void count(std::vector<std::string> &seq, int N);

int main() {
  int N;
  do {
    std::cout << "Enter N: ";
    std::cin >> N;
  } while (N <= 0);
  std::vector<std::string> seq = { "1", "1", "1" };
  if (seq.size() < N) {
    count(seq, N);
  }

  for (auto s : seq) {
    std::cout << s << " ";
  }
  return 0;
}

std::string add(std::string n1, std::string n2) {
  std::string new_number;
  if (n1.length() > n2.length()) {
    while (n2.length() + new_number.length() != n1.length()) {

      new_number += "0";
    }
    n2 = new_number + n2;
  }
  else {
    while (n1.length() + new_number.length() != n2.length()) {

      new_number += "0";
    }
    n1 = new_number + n1;
  }
  // std::cout << n1 << "\t" << n2 << "\n";
  std::string res;
  int digit = 0, sum;
  for (int i = n1.length() - 1; i >= 0; i--) {
    sum = std::stoi(std::string(1, n1[i])) + std::stoi(std::string(1, n2[i])) + digit;
    digit = sum / 10;
    res = std::to_string(sum % 10) + res;
  }
  if (digit > 0) {
    res = std::to_string(digit) + res;
    // std::cout << sum << "\t" << digit << "\n";
  }
  return res;
}

void count(std::vector<std::string> &seq, int N) {
  while (seq.size() != N) {
    seq.push_back(add(add(seq[seq.size() - 3], seq[seq.size() - 2]), seq[seq.size() - 1]));
  }
}