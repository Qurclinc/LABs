#include "BinInOut.h"
#include <iostream>

int main() {
	int n;
	std::cout << "Enter int number: ";
	std::cin >> n;
	std::cout << "Binary represenation: \n";
	BinOut((unsigned char*)&n, sizeof(n));
	std::cout << "Enter binary representation of int number:\n";
	BinIn((unsigned char*)&n, sizeof(n));
	std::cout << "This is its value: " << n << "\n";

	float x;
	std::cout << "Enter float number: ";
	std::cin >> x;
	std::cout << "Binary represenation: \n";
	BinOut((unsigned char*)&x, sizeof(x));
	std::cout << "Enter binary representation of int number:\n";
	BinIn((unsigned char*)&x, sizeof(x));
	std::cout << "This is its value: " << x << "\n";
}