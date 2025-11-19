#include "CountInt.h"

int CountInt::assignments = 0;
int CountInt::comparisions = 0;

CountInt::CountInt(): m_value(0) {
}

CountInt::CountInt(int value): m_value(value) {}

CountInt::~CountInt() {}

CountInt& CountInt::operator= (const CountInt& obj) {
    m_value = obj.m_value;
    CountInt::assignments++;
    return *this;
}

bool CountInt::operator==(const CountInt& obj) {
    CountInt::comparisions++;
    return m_value == obj.m_value;
}

bool CountInt::operator!=(const CountInt& obj) {
    CountInt::comparisions++;
    return !(m_value == obj.m_value); 
}

bool CountInt::operator>(const CountInt& obj) {
    CountInt::comparisions++;
    return m_value > obj.m_value;
}

bool CountInt::operator<(const CountInt& obj) {
    CountInt::comparisions++;
    return obj.m_value > m_value;
}

bool CountInt::operator>=(const CountInt& obj) {
    CountInt::comparisions++;
    return !(m_value < obj.m_value);
}

bool CountInt::operator<=(const CountInt& obj) {
    CountInt::comparisions++;
    return !(m_value > obj.m_value);
}

void CountInt::reset() {
    CountInt::assignments = 0;
    CountInt::comparisions = 0;
}

void CountInt::count() {
    std::cout << "Assignments count: " << CountInt::assignments << "\n";
    std::cout << "Comparitions count: " << CountInt::comparisions << "\n";
}

std::istream& operator>>(std::istream& is, CountInt& obj) {
    int value;
    is >> value;
    obj = CountInt(value);
    return is;
}

std::ostream& operator<<(std::ostream& os, const CountInt& obj) {
    os << obj.m_value;
    return os;
}