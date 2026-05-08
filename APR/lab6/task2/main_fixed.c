#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

bool validate(char* value) {
  char* endptr;
  long input = strtol(value, &endptr, 10);
  if (*endptr != '\0' && !isspace((unsigned char)*endptr)) {
    return false;
  }
  return true;
}

int main(int argc, char* argv[]) {
  --argc;
  if (argc != 2) {
    printf("Необходимо передать 2 целочисленных параметра!\n");
    return -1;
  }
  if (!validate(argv[1])) {
    puts("Первый параметр не целое число\n");
    return -1;
  }
  if (!validate(argv[2])) {
    puts("Второй параметр не целое число\n");
    return -1;
  }
  int x = atoi(argv[1]);
  int y = atoi(argv[2]);
  if (y == 0) {
    puts("Деление на 0\n");
    return -1;
  }

  printf("Результат: %d\n", x / y);
}

