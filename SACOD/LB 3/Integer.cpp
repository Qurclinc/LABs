#include "Integer.h"
#include <cmath>

Integer::Integer() {
    m_number.push_back(0);
}

Integer::Integer(ull num) {
    std::string s = std::to_string(num);
    *this = Integer(s);
}

Integer::Integer(std::string num) {
    int i = num.length();
    while (i > 0) {
        int start = (i - 3 > 0) ? i - 3 : 0;
        m_number.push_back(std::stoi(num.substr(start, i - start)));
        i -= 3;
    }
}

Integer::Integer(std::vector<int> &num) {
    m_number = num;
}

Integer::Integer(const Integer& obj): m_number(obj.m_number), m_d(obj.m_d) {}

Integer Integer::operator=(const Integer& obj) {
    m_number = obj.m_number;
    m_d = obj.m_d;
    return *this;
}

bool Integer::operator==(const Integer &obj) const {
    if (m_number.size() == obj.m_number.size()) {
        for (int i = m_number.size() - 1; i >= 0; i--) {
            if (m_number[i] != obj.m_number[i]){
                return false;
            }
        }
        return true;
    }
    return false;
}

bool Integer::operator>(const Integer &obj) const {
    if (m_number.size() < obj.m_number.size()) {
        return false;
    }
    else if (m_number.size() > obj.m_number.size()) {
        return true;
    }
    else {
        for (int i = m_number.size() - 1; i >= 0; i--) {
            if (m_number[i] > obj.m_number[i]){
                return true;
            }
            else if (m_number[i] < obj.m_number[i]) {
                return false;
            }
        }
    }
    return false;
}

bool Integer::operator!= (const Integer &obj) const{
    return (*this == obj);
}

bool Integer::operator<(const Integer &obj) const {
    return (obj > *this);
}

bool Integer::operator<= (const Integer &obj) const {
    return !(*this > obj);
}

bool Integer::operator>= (const Integer &obj) const {
    return !(*this < obj);
}

Integer Integer::operator+(const Integer &obj) const {
    int buf = 0;
    Integer min, max;
    std::vector<int> res;
    (*this < obj) ? min = *this : min = obj;
    (*this > obj) ? max = *this : max = obj;
    // Сначала происходит поразрядное сложение с меньшим числом, т.к. одно из слагаемых может быть "длиннее"
    for (int i = 0; i < min.m_number.size(); i++) {
        int sum = max.m_number[i] + min.m_number[i];
        res.push_back((sum % m_d) + buf); // При сложении может получиться число большее чем m_d. Потому берется остаток от деления на m_d и прибавляется "буфер"
        buf = sum / m_d; // Тот самый "буфер" который "запоминает" целую часть от деления на m_d для следующего поразрядного сложения
    }
    // Случай, когда одно число "длиннее". Необходимо добавить все его разряды в результат сложения, с учётом что при сложениях ДО этого мог быть непустой "буфер"
    for (int i = min.m_number.size(); i < max.m_number.size(); i++) {
        // В остальном сложение аналогичное
        int sum = max.m_number[i] + buf; 
        res.push_back(sum % m_d);
        buf = sum / m_d;
    }

    if (buf) { // Последнее добавлени "буфера" как например если мы сложим 999+1, чтобы получилось "1000".
        res.push_back(buf);
    }
    return Integer(res);
}

Integer Integer::operator+=(const Integer &obj) {
    *this = *this + obj;
    return *this;
}

Integer Integer::operator-(const Integer &obj) const {
    if (*this < obj) {
        throw "First digit must be higher or equal than second!"; // Было сказано, что длинную арифметику для отрицательных числе не рассматриваем
    }
    int buf = 0;
    std::vector<int> res;
    // Вычитание сильно похоже на сложение: точно таким же образом, мы из большего числа вычитаем меньшее поразрядно
    for (int i = 0; i < obj.m_number.size(); i++) {
        int sub = m_number[i] - obj.m_number[i] - buf;
        if (sub < 0) { // Если результат вычитания отрицателен, то здесь "буфер" осуществляет роль "заёма" из деления столбиком
            buf = 1;
            sub += m_d; // И чтобы разряд не был отрицательным - прибавляем то самое m_d. Очень напоминает вычитание столбиком
        }
        else {
            buf = 0; // Если же на данном этапе результат вычитания оказался неотрицательным, то обнуляем "заём"
        }
        res.push_back(sub);
    }
    // И так как первое число не меньше второго - то в нём вполне может быть больше разрядов. Это тоже нужно учесть при формировании результата
    if (m_number.size() > obj.m_number.size()) {
        for (int i = obj.m_number.size(); i < m_number.size(); i++) {
            int sub = m_number[i] - buf; // Вычитание идёт схожим образом, с учётом "заёма" который мог остаться с прошлого цикла. В остальном суть та же
            if (sub < 0) {
                sub += m_d;
                buf = 1;
            }
            else {
                buf = 0;
            }
            res.push_back(sub);
        }
    }
    // В результате вычитания может образоваться разряд с одним единственным 0. Они же "незначащие нули". Их необходимо удалять
    while (res.size() > 1 && res.back() == 0) {
        res.pop_back();
    }
    return Integer(res);
}

Integer Integer::operator-=(const Integer &obj) {
    *this = *this - obj;
    return *this;
}

Integer Integer::operator* (const Integer &obj) const {
    std::vector<int> res(m_number.size() + obj.m_number.size(), 0); // Здесь для реализации стоит проинициализировать нулями результирующий вектор
    // Если интересно - можете раскомментировать myCout и наглядно проследить операции
    if (*this == Integer(0) || obj == Integer(0)) {
        return Integer(0);
    }
    for (int i = 0; i < m_number.size(); i++) {
        int buf = 0; // Тот самый "буфер"
        int d1 = m_number[i]; // Разряд первого числа
        // Тот самый вложенный цикл, который каждый раз пробегает по второму числу
        for (int j = 0; j < obj.m_number.size(); j++) {
            int d2 = obj.m_number[j]; // Разряд второго числа
            int mult = d1 * d2 + res[i + j] + buf; // Происходит перемножение первого разряда на второй, а затем складывается "буфер" (как в сложении и вычитании)
            // И прибавляется значение в текущем результирующем разряде
            buf = mult / m_d; // Так как мы легко можем вылететь за m_d то сохраняем в буфер излишек
            res[i + j] = mult % m_d; // И берем только остаток, тут все по аналогии
            // std::cout << i << "\t" << j << "\t\t";
            // myCout(res, d1, d2, buf);
        }
        if (buf > 0) {
        res[i + obj.m_number.size()] += buf; // Если остается ненулевой буфер - его тоже следует учесть
        }
    }
    while (res.back() == 0) { // Удаление незначащих нулей
        res.pop_back();
    }
    return Integer(res);
}

Integer Integer::operator*=(const Integer &obj) {
    *this = *this * obj;
    return *this;
}

Integer Integer::operator/(const Integer &obj) const{
    if (obj == Integer("0")) {
        throw "Division by zero!"; // Логично, на ноль не делим
    }
    Integer res; // Результирующее число
    Integer buf; // Тот самый буфер, да не тот самый
    // Цикл проходит по разрядам числа с конца (но так как число хранится в перевёрнутом виде - то считай что с начала)
    for (int i = m_number.size() - 1; i >= 0; i--) {
        buf = buf * Integer(m_d) + Integer(m_number[i]); // Буфер сдвигается на один разряд влево, и к нему прибавляется текущий разряд делимого
        int count = 0; // Счётчик делений
        while (buf >= obj) {
            buf -= obj; // Пока буфер больше чем делитель, мы вычитаем его и копим счётчик
            count++;
        }
        res = res * Integer(m_d) + Integer(count); // Накопление результата
    }
    // Избавление от незначащих нулей
    while (res.m_number.size() > 1 && res.m_number.back() == 0) {
        res.m_number.pop_back(); 
    }
    return res;
}

Integer Integer::operator/=(const Integer &obj) {
    *this = *this / obj;
    return *this;
}

Integer Integer::operator%(const Integer &obj) const {
    // Остаток можно взять путем умножение деления нацело на делитель, и вычитанием результата из делимого. Операции уже реализованы
    return *this - ((*this / obj) * obj);
}

Integer Integer::operator%=(const Integer &obj) {
    *this = *this % obj;
    return *this;
}

Integer Integer::operator^(const Integer &obj) const {
    // Возведение в степен реализовано с помощью QuickPow - быстрого возведения в степень
    Integer f = 1; // Результат
    Integer c = *this; // Основание
    Integer k = obj; // Степень
    while (k > 0) { 
        // Если степень чётная, то основание возводится в квадрат, а степень делится на 2
        if (k % 2 == 0) {
            c *= c;
            k /= 2;
        }
        // В противном случае результат умножается на основание, а из степени вычитается 1
        else {
            f *= c;
            k -= 1;
        }
    }
    return f;
}

void Integer::print() const
{
    for (int i = m_number.size() - 1; i >= 0; i--) {
        std::string buf = std::to_string(m_number[i]);
        if (buf.length() != 3 && i != m_number.size() - 1) {
            buf = std::string(3 - buf.length(), '0') + buf;
        }
        std::cout << buf;

    }
    std::cout << "\n";
}

std::istream& operator>> (std::istream& is, Integer& obj) {
    std::string str;
    is >> str;
    obj = Integer(str);
    return is;
}

std::ostream& operator<< (std::ostream& os, const Integer& obj) {
    for (int i = obj.m_number.size() - 1; i >= 0; i--) {
        std::string buf = std::to_string(obj.m_number[i]);
        if (buf.length() != 3 && i != obj.m_number.size() - 1) {
            buf = std::string(3 - buf.length(), '0') + buf;
        }
        os << buf;

    }
    os << "\0";
    return os;
}

void Integer::myCout(std::vector<int> &vec, int d1, int d2, int buf) const{
    for (auto i: vec) {
        std::cout << i << "\t";
    }
    std::cout << "\n" << d1 << "\t" << d2 << "\t" << buf << "\n\n";
}