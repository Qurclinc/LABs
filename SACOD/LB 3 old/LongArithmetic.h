#include <string>
#include <iostream>

class LongArithmetic {
private:
    std::string m_n;
public:
    LongArithmetic(int n);
    LongArithmetic(std::string n);
    LongArithmetic(const char* n);
    LongArithmetic(const LongArithmetic &n);

    LongArithmetic operator+(const LongArithmetic &n2);
    LongArithmetic operator+=(const LongArithmetic &n2);


    void set(int n) { m_n = std::to_string(n); }
    void set(std::string n) { m_n = n; }
    std::string get() const { return m_n; }
    void print() const { std::cout << m_n; }
};