#pragma once
#include <chrono>
#include <cstdio>
#include <ctime>
#include <thread>

// input 1 byte
static inline unsigned char inb() {
	return static_cast<unsigned char>(std::getchar());
}

// output 1 byte
static inline void outb(const unsigned char data) {
	return static_cast<void>(std::putchar(data));
}

// input a long integer
static inline unsigned long inl() {
	unsigned long ret = 0;
	unsigned char ch;
	int sign = 0;
	while ((ch = inb()))
		if (ch != '\n' && ch != ' ' && ch != '\t')
			break;
	do {
		if (ch == '-' && !sign)
			sign = 1;
		else if (ch < '0' || ch > '9')
			break;
		ret = ret * 10 + ch - '0';
	} while ((ch = inb()));
	return sign ? -ret : ret;
}

// input a string
static inline void getstr(char *data) {
	char c;
	int i = 0;
	while ((c = inb()) != '\n')
		data[i++] = c;
	data[i] = '\0';
}

// convert a char to unsigned int
static inline unsigned int ord(char data) { return (unsigned int) data; }

// output an integer
static inline void outl(const int data) {
	unsigned char str[12];
	int tmp = data;
	int i = 0, s = 0;
	if (tmp < 0) {
		s = 1;
		tmp = -tmp;
	}
	do {
		str[i++] = tmp % 10 + '0';
	} while ((tmp /= 10) > 0);
	if (s)
		str[i++] = '-';
	while (i--) {
		outb(str[i]);
	}
}

// output a string
static inline void print(const char *str) {
	for (; *str; str++)
		outb(*str);
}

// output a string with a newline
static inline void println(const char *str) {
	print(str);
	outb('\n');
}

// output an integer
static inline void outlln(const unsigned int data) {
	outl(data);
	outb('\n');
}
