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
        # print(answers)
    return answers
        

if __name__ == "__main__":
    # A = np.array([
    #     np.array(list(map(float, [3, -5, 3, 1]))),
    #     np.array(list(map(float, [1, 2, 1, 4]))),
    #     np.array(list(map(float, [2, 7, -1, 8])))
    # ])
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09, 0.83]),
        np.array([0.16, 0.24, -1, -0.35, -1.21]),
        np.array([0.23, -0.08, 0.05, -0.75, -0.65]),
        np.array([-0.86, 0.23, 0.18, 0.17, 1.42])
    ])
    print(A)
    print("\n\n")
    AA = trianglize(A)    
    print(AA)
    res = reverse(AA)
    for k, v in res.items():
        print(float(v))