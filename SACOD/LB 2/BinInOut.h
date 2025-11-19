#pragma once
#include <conio.h>
#include <stdio.h>

void BinOut(unsigned char* Buf, int len) {
	int i, j;
	unsigned char byte;
	for (i = len - 1; i >= 0; i--) {
		for (j = 1, byte = Buf[i]; j <= 8; byte <<= 1, j++) {
			_putch(byte & 0x80 ? '1' : '0');
		}
	}
	printf("\n");
}

void BinIn(unsigned char* Buf, int len) {
	int i, j;
	char ch;
	for (i = len - 1; i >= 0; i--) {
		for (j = 1, Buf[i] = 0; j <= 8; Buf[i] = (Buf[i] << 1) + (ch - '0'), j++) {
			while ((ch = _getch()) != '0' && ch != '1');
			_putch(ch);
		}
	}
	printf("\n");
}