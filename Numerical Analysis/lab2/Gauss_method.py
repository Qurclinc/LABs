import numpy as np

def trianglize(matrix: np.array) -> np.array:
    for i in range(len(matrix)):
        matrix[i] /= matrix[i][i]
        for j in range(i + 1, len(matrix)):
            matrix[j] -= matrix[i] * matrix[j][i]
    return matrix

def reverse(matrix: np.array) -> np.array:
    answers = dict()
    for i in range(len(matrix) - 1, -1, -1):
        res = matrix[i][-1]
        for j in range(len(matrix)):
            if answers.get(j):
                res -= matrix[i][j] * answers[j]
        answers[i] = res
        print(answers)
        

if __name__ == "__main__":
    # A = np.array([
    #     np.array(list(map(float, [3, -5, 3, 1]))),
    #     np.array(list(map(float, [1, 2, 1, 4]))),
    #     np.array(list(map(float, [2, 7, -1, 8])))
    # ])
    A = np.array([
        np.array([2.34, -4.21, -11.61, 14.41]),
        np.array([8.04, 5.22, 0.27, -6.44]),
        np.array([3.92, -7.99, 8.37, 55.56])
    ])
    print(A)
    print("\n\n")
    AA = trianglize(A)    
    print(AA)
    reverse(AA)