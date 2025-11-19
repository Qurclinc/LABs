from typing import List
import random

def generate_matrix(M: int, N: int, seed: int = None) -> List[List[int]]:
    if seed:
        random.seed(seed)
    return [[random.randint(-50, 51) for _ in range(N)] for _ in range(M)]

def find_matrix_sum(matrix: List[List[int]]):
    return sum(sum(line) for line in matrix)

def get_negative_elements(matrix: List[List[int]]) -> List[tuple]:
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < 0:
                result += [(matrix[i][j], i, j)]
    return sorted(result, key=lambda x: x[0])

def zero_out(matrix: List[List[int]], negatives: List[tuple]):
    i, j = negatives[0][1], negatives[0][2]
    negatives.pop(0)
    matrix[i][j] = 0

def main():
    matrix = generate_matrix(5, 5, 2011)
    print(*matrix, sep="\n")
    negatives = get_negative_elements(matrix)
    success = False
    while True:
        if find_matrix_sum(matrix) > 0:
            success = True
            break
        if len(negatives) == 0:
            break
        zero_out(matrix, negatives)
    print()
    print(*matrix, sep="\n") if success else print("Невозможно сделать сумму положительной.")
        
if __name__  == "__main__":
    main()