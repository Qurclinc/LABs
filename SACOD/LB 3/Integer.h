#include <iostream>
#include <vector>
#include <string>

typedef unsigned long long ull;

class Integer {
private:
    int m_d = 1000;
protected:
    std::vector<int> m_number;

public:
    Integer();
    Integer(ull num);
    Integer(std::string num);
    Integer(std::vector<int> &num);
    Integer(const Integer &obj);

    Integer operator=(const Integer &obj);
    bool operator==(const Integer &obj) const;
    bool operator>(const Integer &obj) const;

    bool operator!=(const Integer &obj) const;
    bool operator>=(const Integer &obj) const;
    bool operator<(const Integer &obj) const;
    bool operator<=(const Integer &obj) const;

    Integer operator+(const Integer &obj) const;
    Integer operator-(const Integer &obj) const;
    Integer operator*(const Integer &obj) const;
    Integer operator/(const Integer &obj) const;
    Integer operator%(const Integer &obj) const;
    Integer operator^(const Integer &obj) const;

    Integer operator+=(const Integer &obj);
    Integer operator-=(const Integer &obj);
    Integer operator*=(const Integer &obj);
    Integer operator/=(const Integer &obj);
    Integer operator%=(const Integer &obj);

    friend std::istream& operator>> (std::istream& is, Integer& obj);
    friend std::ostream& operator<< (std::ostream& is, const Integer& obj);
    void print() const;

private:
    void myCout(std::vector<int> &vec, int d1, int d2, int buf) const;
};