#include "LongArithmetic.h"

LongArithmetic::LongArithmetic(int n): m_n(std::to_string(n)) {}
LongArithmetic::LongArithmetic(std::string n): m_n(n) {}
LongArithmetic::LongArithmetic(const char* n): m_n(std::string(n)) {}
LongArithmetic::LongArithmetic(const LongArithmetic &n): m_n(n.get()) {}

LongArithmetic LongArithmetic::operator+(const LongArithmetic &n2) {
    std::string new_number;
    std::string n = n2.get();
    if (m_n.length() > n.length()) {
        while (n.length() + new_number.length() != m_n.length()) {
        new_number += "0";
    }
        n = new_number + n;
    }
    else {
        while (m_n.length() + new_number.length() != n.length()) {

        new_number += "0";
        }
        m_n = new_number + m_n;
    }
    // std::cout << n1 << "\t" << n2 << "\n";
    std::string res;
    int digit = 0, sum;
    for (int i = m_n.length() - 1; i >= 0; i--) {
        sum = std::stoi(std::string(1, m_n[i])) + std::stoi(std::string(1, n[i])) + digit;
        digit = sum / 10;
        res = std::to_string(sum % 10) + res;
    }
    if (digit > 0) {
        res = std::to_string(digit) + res;
        // std::cout << sum << "\t" << digit << "\n";
    }
    return LongArithmetic(res);
}

LongArithmetic LongArithmetic::operator+=(const LongArithmetic &n2) {
    return *this = *this + n2;
}

