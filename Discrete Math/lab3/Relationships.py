def transpose_matrix(matrix):
    result = [[] for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            result[i] += [matrix[j][i]]
    return result

def generate_matrix(universum, set):
    matrix = [[0 for _ in range(len(universum.arr))] for _ in range(len(universum.arr))]
    for elem in set.arr:
        matrix[elem[0] - 1][elem[1] - 1] = 1
    return matrix

# No needs
# def reverse_matrix(matrix):
#     return [[(0 if elem == 1 else 1) for elem in line] for line in matrix]

# No needs (x2)
# def multiple_matrix(matrix):
#     res = [[0 for i in range(len(matrix))] for _ in range(len(matrix))]
#     for i in range(len(matrix)):
#         for j in range(len(matrix)):
#             for k in range(len(matrix)):
#                 res[i][j] += matrix[i][k] * matrix[k][j]
#     return res


def check_reflecsive(universum, set):
    matrix = generate_matrix(universum, set)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                if matrix[i][j] != 1:
                    return False
    return True
    # print(*matrix, sep="\n")

def check_anti_reflecsive(universum, set):
    matrix = generate_matrix(universum, set)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                if matrix[i][j] == 1:
                    return False
    return True

# Неоптимально, можно и проще. Но ради разнообразия другой алгоритм
def check_symmetry(universum, set):
    matrix = generate_matrix(universum, set)
    transposed_matrix = transpose_matrix(matrix)
    return matrix == transposed_matrix

def check_anti_symmetry(universum, set):
    matrix = generate_matrix(universum, set)
    # print(*matrix, sep="\n")
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == matrix[j][i] == 1 and i != j:
                return False
    return True
    
def check_transitivity(universum, set):
    matrix = generate_matrix(universum, set)
    # print(*matrix, sep="\n", end="\n\n\n")
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                for k in range(len(matrix)):
                    # print(i + 1, j + 1, k + 1)
                    if matrix[j][k] == 1 and matrix[i][k] != 1:
                            # print("!!!", i + 1, j + 1, k + 1)
                            return False
    return True

def check_anti_transitivity(universum, set):
    matrix = generate_matrix(universum, set)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                for k in range(len(matrix)):
                    if matrix[j][k] == 1 and matrix[i][k] == 1:
                        return False
    return True