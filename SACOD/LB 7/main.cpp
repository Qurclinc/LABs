#include <iostream>
#include "Stack.h"
#include "Heap.h"
#include <cstdlib>

void menu();
void stackMenu();
void heapMenu();
template <class T>
void stackWork(Stack<T>& stack);
template <class T>
void heapWork(Heap<T>& heap);
void await();

int main() {
    int choice;
    Stack<int> stack;
    Heap<int> heap;
    do {
        menu();
        std::cin >> choice;
        switch (choice) {
        case 1:
            stackWork(stack);
            break;
        case 2:
            heapWork(heap);
            break;
        case 0:
            std::cout << "Exiting...\n";
            break;
        default:
            std::cout << "Invalid choice!\n";
            await();
            break;
        }
    } while (choice != 0);
}

void menu() {
    system("clear");
    std::cout << "=====================================================\n";
    std::cout << "1) Stack Operations\n";
    std::cout << "2) Heap Operations\n";
    std::cout << "0) Exit\n";
    std::cout << "=====================================================\n";
    std::cout << "-> ";
}

void stackMenu() {
    system("clear");
    std::cout << "=====================================================\n";
    std::cout << "1) Push element\n";
    std::cout << "2) Pop element\n";
    std::cout << "3) Get top\n";
    std::cout << "4) Check if empty\n";
    std::cout << "5) Get size\n";
    std::cout << "6) Print stack\n";
    std::cout << "0) Back to main menu\n";
    std::cout << "=====================================================\n";
    std::cout << "-> ";
}

void heapMenu() {
    system("clear");
    std::cout << "=====================================================\n";
    std::cout << "1) Push element\n";
    std::cout << "2) Extract root\n";
    std::cout << "3) Get top (peek)\n";
    std::cout << "4) Remove element\n";
    std::cout << "5) Replace element\n";
    std::cout << "6) Print heap\n";
    std::cout << "0) Back to main menu\n";
    std::cout << "=====================================================\n";
    std::cout << "-> ";
}

template <class T>
void stackWork(Stack<T>& stack) {
    int choice;
    T elem;
    do {
        stackMenu();
        std::cin >> choice;
        switch (choice) {
        case 1:
            std::cout << "Enter element to push: ";
            std::cin >> elem;
            stack.push(elem);
            std::cout << "Element pushed.\n";
            await();
            break;
        case 2:
            if (!stack.empty()) {
                stack.pop();
                std::cout << "Element popped.\n";
            } else {
                std::cout << "Stack is empty.\n";
            }
            await();
            break;
        case 3:
            try {
                std::cout << "Top element: " << stack.top() << "\n";
            } catch (const char* msg) {
                std::cout << msg << "\n";
            }
            await();
            break;
        case 4:
            std::cout << (stack.empty() ? "Stack is empty.\n" : "Stack is not empty.\n");
            await();
            break;
        case 5:
            std::cout << "Stack size: " << stack.size() << "\n";
            await();
            break;
        case 6:
            std::cout << "Stack contents: ";
            stack.print();
            await();
            break;
        case 0:
            break;
        default:
            std::cout << "Invalid choice!\n";
            await();
            break;
        }
    } while (choice != 0);
}

template <class T>
void heapWork(Heap<T>& heap) {
    int choice;
    T elem, key, value;
    do {
        heapMenu();
        std::cin >> choice;
        switch (choice) {
        case 1:
            std::cout << "Enter element to push: ";
            std::cin >> elem;
            heap.push(elem);
            std::cout << "Element pushed.\n";
            await();
            break;
        case 2:
            if (!heap.empty()) {
                elem = heap.extractRoot();
                std::cout << "Extracted root: " << elem << "\n";
            } else {
                std::cout << "Heap is empty.\n";
            }
            await();
            break;
        case 3:
            if (!heap.empty()) {
                std::cout << "Top element (peek): " << heap.peek() << "\n";
            } else {
                std::cout << "Heap is empty.\n";
            }
            await();
            break;
        case 4:
            std::cout << "Enter element to remove: ";
            std::cin >> elem;
            heap.remove(elem);
            std::cout << "Element removed if it existed.\n";
            await();
            break;
        case 5:
            std::cout << "Enter element to replace: ";
            std::cin >> key;
            std::cout << "Enter new value: ";
            std::cin >> value;
            heap.replace(key, value);
            std::cout << "Element replaced if it existed.\n";
            await();
            break;
        case 6:
            std::cout << "Heap contents: ";
            heap.print();
            await();
            break;
        case 0:
            break;
        default:
            std::cout << "Invalid choice!\n";
            await();
            break;
        }
    } while (choice != 0);
}

// Ожидание пользователя
void await() {
    std::cin.ignore();
    std::cin.get();
}
