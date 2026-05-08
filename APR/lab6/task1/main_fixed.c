#include <stdio.h>

int main() {
  char buffer[8];

  printf("%s", "Введите строку: ");
  scanf("%7s", buffer);

  printf("Вы ввели: %s\n", buffer);
  return 0;
}

