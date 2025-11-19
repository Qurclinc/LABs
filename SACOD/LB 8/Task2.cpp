#include <iostream>
#include <vector>

/*
Решить судоку размером 4*4. Задана частично заполненная матрица,
размером 4*4. В ней необходимо расставить числа от 1 до 4, так чтобы в
каждой строке, в каждом столбце и в каждом маленьком квадрате не было
одинаковых цифр.
*/

void print(std::vector<std::vector<int>> &sudoku) {
    for (auto row: sudoku) {
        for (auto elem: row) {
            std::cout << elem << " ";
        }
        std::cout << "\n";
    }
}

bool validate(std::vector<std::vector<int>> &sudoku, int row, int col, int num) {
    int N = 2;
    for (int y = 0; y < sudoku.size() - 1; y++) {
        if (sudoku[row][y] == num) {
            return false;
        }
    }

    for (int x = 0; x < sudoku.size() - 1; x++) {
        if (sudoku[x][col] == num) {
            return false;
        }
    }

    int start_row = row - row % N;
    int start_col = col - col % N;
    for (int x = start_row; x < N; x++) {
        for (int y = start_col; y < N; y++) {
            if (sudoku[x + start_row][y + start_col] == num) {
                return false;
            }
        }
    }
    return true;
}

bool solveSudoku(std::vector<std::vector<int>> &sudoku, int row, int col) {
    if (row == sudoku.size() - 1 && col == sudoku.size()) {
        return true;
    }

    if (col == sudoku.size()) {
        row++;
        col = 0;
    }

    if (sudoku[row][col] > 0) {
        return solveSudoku(sudoku, row, col + 1);
    }

    for (int num = 1; num <= sudoku.size(); num++) {
        if (validate(sudoku, row, col, num)) {
            sudoku[row][col] = num;
            if (solveSudoku(sudoku, row, col + 1)) {
                return true;
            }
        }
        sudoku[row][col] = 0;
    }
    return false;
}

int main() {
    std::vector<std::vector<int>> sudoku {
        {0, 0, 2, 0},
        {0, 1, 0, 4},
        {4, 0, 1, 0},
        {0, 2, 0, 0}
    };
    if (solveSudoku(sudoku, 0, 0)) {
        print(sudoku);
    } else {
        std::cout << "No solutions exists.\n";
    }
    return 0;
}