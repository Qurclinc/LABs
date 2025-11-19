#pragma once
#include "List.h"

template <class T>
class Stack {
private:

    List<T> list;

public:

    Stack() {}
    Stack(const Stack &obj): list(obj.list) {};

    Stack& operator= (const Stack &obj) {
        list = obj.list;
    }

    void push(T value) {
        list.push_back(value);
    }

    void pop() {
        list.pop_back();
    }

    T top() {
        if (!empty()) {
            return list.back();
        } else {
            throw "Stack is empty";
        }
    }

    bool empty() {
        return list.isEmpty();
    }

    int size() {
        int len = 0;
        List<T> copy = list;
        while (!copy.isEmpty()) {
            copy.pop_back();
            len++;
        }
        return len;
    }

    void print() {
        list.print();
    }
};