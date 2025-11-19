#include <iostream>
#include <math.h>

unsigned long long fact(unsigned long long num) {
  if (num == 0) {
    return 1;
  }
  if (num == 1) {
    return 1;
  }
  return num * fact(num - 1);
}

bool check(unsigned long long num) {
  unsigned long long sum = 0, r_num = num;
  while (num != 0) {
    sum += fact(num % 10);
    num /= 10;
  }
  return sum == r_num;
}

int main() {
  for (unsigned long long i = 1; i < __LONG_LONG_MAX__; i++) {
    if (check(i)) {
      printf("%d\n", i);
    }
  }
  return 0;
}