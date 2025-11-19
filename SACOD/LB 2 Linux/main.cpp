#include "BinInOut.h"
#include <iostream>

enum Latin {
    I = 1,
    V = -5,
    X = 10,
    L = 50,
    C = 100,
    D = 500,
    M = 1000
};

void doShort();
void doFloat();
void doEnum();
void showBinaryRepresentation(Latin value);
void menu();


int main() {
    char choice;
    do {
        menu();
        std::cin >> choice;
        switch (choice) {
            case '1':
                system("clear");
                doShort();
                std::cin.ignore();
                std::cin.get();
                break;
            case '2':
                system("clear");
                doFloat();
                std::cin.ignore();
                std::cin.get();
                break;
            case '3':
                system("clear");
                doEnum();
                std::cin.ignore();
                std::cin.get();
                break;
            case '0':
                system("clear");
                std::cout << "Finishing...";
                std::cin.ignore();
                std::cin.get();
                break;
            default:
                std::cout << "Unknown command";
                std::cin.ignore();
                std::cin.get();
                break;
            }
    } while (choice != '0');
    return 0;
}

void doShort() {
    short x;
    std::cout << "Enter short x: ";
    std::cin >> x;
    std::cout << "Binary representation:\n";
    BinOut((unsigned char*)&x, sizeof(x));
    std::cout << "Enter binary representation of short:\n";
    BinIn((unsigned char*)&x, sizeof(x));
    std::cout << "This is its value: " << x << "\n";
}

void doFloat() {
    float x;
    std::cout << "Enter float x: ";
    std::cin >> x;
    std::cout << "Binary representation:\n";
    BinOut((unsigned char*)&x, sizeof(x));
    std::cout << "Enter binary representation of float:\n";
    BinIn((unsigned char*)&x, sizeof(x));
    std::cout << "This is its value: " << x << "\n";
}

void doEnum() {
    showBinaryRepresentation(I);
    showBinaryRepresentation(V);
    showBinaryRepresentation(X);
    showBinaryRepresentation(L);
    showBinaryRepresentation(C);
    showBinaryRepresentation(D);
    showBinaryRepresentation(M);
}

void showBinaryRepresentation(Latin value) {
    std::cout << "Binary representation of " << value << ":\n";
    BinOut((unsigned char*)&value, sizeof(value));
}

void menu() {
    system("clear");
    std::cout << "====================================\n";
    std::cout << "Choose command:\n";
    std::cout << "1) short\n";
    std::cout << "2) float\n";
    std::cout << "3) Latin (enum)\n";
    std::cout << "0) exit\n";
    std::cout << "====================================\n";
    std::cout << "-> ";
}