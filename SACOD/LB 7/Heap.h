#pragma once
#include <vector>

template <class T>
class Heap {
private:
    std::vector<T> m_arr;
public:
    Heap() {}
    Heap(std::vector<T> arr): m_arr(arr) {
        buildHeap();
    }
    Heap(const Heap &obj) {
        copy(obj);
    }
    ~Heap() {}

    Heap& operator=(const Heap &obj) {
        copy(obj);
        return *this;
    }

    void push(T elem) {
        m_arr.push_back(elem);
        buildHeap();
    }

    T extractRoot() {
        T elem = m_arr.front();
        m_arr.erase(m_arr.begin(), m_arr.begin() + 1);
        buildHeap();
        return elem;
    }

    T peek() {
        return m_arr.front();
    }

    void remove(T elem) {
        for (int i = 0; i < m_arr.size(); i++) {
            if (m_arr[i] == elem) {
                m_arr.erase(m_arr.begin() + i);
                buildHeap();
                return;
            }
        }
    }

    bool empty() {
        return (m_arr.size() == 0);
    }

    void print() {
        if (m_arr.empty()) {
            std::cout << "Heap is empty";
            return;
        }
        for (T elem: m_arr) {
            std::cout << elem << " ";
        }
        std::cout << "\n";
    }

    void replace(T key, T value) {
        for (int i = 0; i < m_arr.size(); i++) {
            if (m_arr[i] == key) {
                m_arr[i] = value;
                buildHeap();
                return;
            }
        }
    }

private:
    void heapify(int n, int i) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;

        if (l < n && m_arr[l] > m_arr[largest]) {
            largest = l;
        }

        if (r < n && m_arr[r] > m_arr[largest]) {
            largest = r;
        }

        if (largest != i) {
            std::swap(m_arr[i], m_arr[largest]);
            heapify(n, largest);
        }

    }

    void buildHeap() {
        for (int i = (m_arr.size() / 2 - 1); i >= 0; i--) {
            heapify(m_arr.size(), i);
        }
    }

    void copy(const Heap &obj) {
        m_arr = obj.m_arr;
    }
};