#include <iostream>
#include <vector>

#include <fstream>
#include <sstream>

#include <cstring>

#include <cmath>

// Define the maze size
const int length = 16;  // Change this to match the size of your maze

// Load data from CSV file
template<typename T>
void load_csv(const std::string& filename, std::vector<std::vector<T>>& data) {
    std::ifstream file(filename);
    if (!file) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::vector<T> row;
        std::stringstream ss(line);
        T value;
        while (ss >> value) {
            row.push_back(value);
            if (ss.peek() == ',') {
                ss.ignore();
            }
        }
        data.push_back(row);
    }
}

int main() {
    std::vector<std::vector<int>> H_walls, V_walls;
    
    // Load data from CSV files
    load_csv("design/H0.csv", H_walls);
    load_csv("design/V0.csv", V_walls);
    
    // Create maze matrix
    std::vector<std::vector<int>> maze(length, std::vector<int>(length, -1));
    
    // Set destination to 0
    if (length % 2 == 1) {
        maze[length / 2][length / 2] = 0;
    } else if (length % 2 == 0) {
        maze[length / 2][length / 2] = 0;
        maze[length / 2][length / 2 - 1] = 0;
        maze[length / 2 - 1][length / 2] = 0;
        maze[length / 2 - 1][length / 2 - 1] = 0;
    }
    
    // Perform Flood Fill
    for (int value = 0; value < 200; ++value) {
        for (int i = 0; i < maze.size(); ++i) {
            for (int j = 0; j < maze[i].size(); ++j) {
                if (maze[i][j] == value) {
                    try {
                        if (V_walls[i][j + 1] != -1 && maze[i][j + 1] == -1) {
                            maze[i][j + 1] = value + 1;
                        }
                    } catch (...) {}
                    
                    try {
                        if (V_walls[i][j] != -1 && maze[i][j - 1] == -1) {
                            maze[i][j - 1] = value + 1;
                        }
                    } catch (...) {}
                    
                    try {
                        if (H_walls[i + 1][j] != -1 && maze[i + 1][j] == -1) {
                            maze[i + 1][j] = value + 1;
                        }
                    } catch (...) {}
                    
                    try {
                        if (H_walls[i][j] != -1 && maze[i - 1][j] == -1) {
                            maze[i - 1][j] = value + 1;
                        }
                    } catch (...) {}
                }
            }
        }
    }
    
    // Print the maze
    for (const auto& row : maze) {
        for (int cell : row) {
            std::cout << cell << '\t';
        }
        std::cout << '\n';
    }
    
    return 0;
}
