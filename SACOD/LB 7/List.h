#pragma once

template <class T>
class Node {
public:
    T m_data;
    Node* next;
    Node* prev;

    Node(T data): next(nullptr), prev(nullptr), m_data(data) {}
};

template <class T>
class List {
private:

    Node<T>* head;
    Node<T>* tail;

public:

    List() {
        head = nullptr;
        tail = nullptr;
    }

    List(const List& obj): head(nullptr), tail(nullptr) {
        copy(obj);
    }

    ~List() {
        while (!isEmpty()) {
            pop_back();
        }
    }

    List& operator=(const List& obj) {
        copy(obj);
        return *this;
    }

    T front() const {
        if (!isEmpty()) {
            return head->m_data;
        } else {
            throw "Stack is empty";
        }
    }

    T back() const {
        if (!isEmpty()) {
            return tail->m_data;
        } else {
            throw "List is empty"; 
        }
    }

    void pop_back() {
        if (!isEmpty()) {
            Node<T>* rem = tail;
            if (head == tail) {
                head = nullptr;
                tail = nullptr;
            } else {
                tail->prev->next = nullptr;
                tail = tail->prev;
            }
            delete rem;
        }
    }

    void pop_front() {
        if (!isEmpty()) {
            Node<T>* rem = head;
            if (head == tail) {
                head = nullptr;
                tail = nullptr;
            } else {
                head->next->prev = nullptr;
                head = head->next;
            }
            delete rem;
        }
    }

    void push_back(T data) {
        Node<T>* obj = new Node<T>(data);
        if (head == nullptr) {
            head = obj;
            tail = obj;
        } else {
            tail->next = obj;
            obj->prev = tail;
            tail = obj;
        }
    }

    void push_front(T data) {
        Node<T>* obj = new Node<T>(data);
        if (head == nullptr) {
            head = obj;
            tail = obj;
        } else {
            head->prev = obj;
            obj->next = head;
            head = obj;
        }
    }

    void print(char delimiter=' ', char end='\n') const {
        if (!isEmpty()) {
            Node<T>* current = head;
            while (current != nullptr) {
                std::cout << current->m_data << delimiter;
                current = current->next;
            }
            std::cout << end;
        } else {
            std::cout << "Stack is empty";
        }
    }

    bool isEmpty() const {
        return head == nullptr;
    }

private:
    void copy(const List& obj) {
        Node<T>* current = obj.head;
        while (current != nullptr) {
            this->push_back(current->m_data);
            current = current->next;
        }
    }
};