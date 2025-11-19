import math
import random
from typing import List

def generate_matrix(M: int, N: int, seed: int = None) -> List[List[int]]:
    if seed:
        random.seed(seed)
    return [[random.randint(-50, 51) for _ in range(N)] for _ in range(M)]

def zero_out(matrix: List[List[int]]):
    for i in range(0, math.ceil(len(matrix) / 2)):
        for j in range(0 + i, len(matrix[i]) - i):
            matrix[i][j] = 0

def main():
    matrix = generate_matrix(5, 5, 200)
    print(*matrix, sep="\n")
    zero_out(matrix)
    print()
    print(*matrix, sep="\n")
    
if __name__ == "__main__":
    main()