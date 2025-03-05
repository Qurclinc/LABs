#include <iostream>
#include <math.h>
#include <string>

bool validateSystem(std::string num, int base) {
  while (num.length() != 0) {
    if ((num[num.length() - 1] - '0') >= base) {
      return true;
    }
    num = num.substr(0, num.length() - 1);
  }
  return false;
}

int toDecimal(std::string n, int base) {
  int s = n[0] - '0';
  for (int i = 1; i < n.length(); i++) {
    s *= base;
    s += n[i] - '0';
  }
  return s;
}

std::string fromDecimal(int n, int base) {
  std::string s = "";
  while (n > 0) {
    s = std::to_string(n % base) + s;
    n /= base;
  }
  return s;
}

int main() {
  int m = 8, n = 6;
  std::string num;
  do {
    printf("Enter number in %d number system: ", m);
    std::getline(std::cin, num);
  } while (validateSystem(num, m));
  // } while (num == "");
  std::cout << "result = " << fromDecimal(toDecimal(num, 8), 6) << "\n";
  return 0;
}