#pragma once
#include <iostream>

class CountInt {
public:
    
    static int comparisions;
    static int assignments;

    int m_value;

    CountInt();
    CountInt(int value);
    ~CountInt();

    CountInt& operator= (const CountInt& obj);
    bool operator== (const CountInt& obj);
    bool operator!= (const CountInt& obj);
    bool operator> (const CountInt& obj);
    bool operator>= (const CountInt& obj);
    bool operator<= (const CountInt& obj);
    bool operator< (const CountInt& obj);
    
    static void reset();
    static void count();
    
    friend std::istream& operator>>(std::istream& is, CountInt& obj);
    friend std::ostream& operator<<(std::ostream& os, const CountInt& obj);
};



