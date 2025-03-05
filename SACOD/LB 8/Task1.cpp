#include <iostream>
#include <vector>
#include <stack>

using namespace std;

// Направления для перемещения: вверх, вправо, вниз, влево
const vector<pair<int, int>> directions = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

bool isValidMove(int x, int y, const vector<vector<int>>& maze, vector<vector<bool>>& visited) {
    int rows = maze.size();
    int cols = maze[0].size();
    return x >= 0 && x < rows && y >= 0 && y < cols && maze[x][y] == 0 && !visited[x][y];
}

bool findPath(vector<vector<int>>& maze, int startX, int startY, vector<pair<int, int>>& path) {
    int rows = maze.size();
    int cols = maze[0].size();
    
    vector<vector<bool>> visited(rows, vector<bool>(cols, false));
    stack<pair<int, int>> backtrackStack;

    backtrackStack.push({startX, startY});
    visited[startX][startY] = true;

    while (!backtrackStack.empty()) {
        auto [x, y] = backtrackStack.top();
        path.push_back({x, y});

        // Проверка, достигли ли выхода
        if (x == 0 || y == 0 || x == rows - 1 || y == cols - 1) {
            return true;
        }

        bool moved = false;
        for (const auto& dir : directions) {
            int newX = x + dir.first;
            int newY = y + dir.second;

            if (isValidMove(newX, newY, maze, visited)) {
                backtrackStack.push({newX, newY});
                visited[newX][newY] = true;
                moved = true;
                break;
            }
        }

        if (!moved) {
            // Нет доступных направлений, возвращаемся назад
            path.pop_back();
            backtrackStack.pop();
        }
    }

    return false; // Путь не найден
}

int main() {
    // Пример лабиринта
    vector<vector<int>> maze = {
        {1, 1, 1, 1, 1, 1, 1, 1, 0, 1},
        {1, 0, 1, 1, 1, 1, 0, 1, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 1, 0, 1},
        {1, 1, 0, 0, 1, 1, 0, 0, 0, 1},
        {1, 1, 1, 1, 1, 1, 0, 1, 1, 1},
        {1, 1, 1, 1, 0, 0, 0, 0, 1, 1},
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
    };

    int startX = 2, startY =  2; // Начальная точка
    vector<pair<int, int>> path;

    if (findPath(maze, startX, startY, path)) {
        cout << "Путь найден:" << endl;
        for (const auto& p : path) {
            cout << "(" << p.first << ", " << p.second << ") ";
        }
        cout << endl;
    } else {
        cout << "Пути нет." << endl;
    }

    return 0;
}
