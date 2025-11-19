#include <iostream>

// Введите год рождения и текущий год. Программа должна вычислить и вывести на экран примерное число
// прожитых человеком дней (без учета високосных лет), если в году 365 дней.

int main() {
    int birthYear = 2005;
    int currentYear = 2025;
    int daysInYear = 365;
    int days = (currentYear - birthYear) * daysInYear;
    std::cout << days << "\n";
}