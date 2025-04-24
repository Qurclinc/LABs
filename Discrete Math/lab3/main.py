from Set import Set
from Relationships import check_reflecsive, check_anti_reflecsive, \
                        check_symmetry, check_anti_symmetry, check_transitivity, \
                        check_anti_transitivity, generate_matrix

# P = Set(
#     [[1, 2],[2, 1],[1, 3],[1, 5],[2, 3],[3, 1],[3, 2],[5, 1],[5, 3],[5, 4]]
# )

# P = Set( # Symmetric
#     [[1,1], [2,2], [3,3], [4,4], [5,5], [1,2], [2,1], [3,2], [2,3], [2,4], [4,2], [1,5], [5,1]]
# )

# P = Set(
#     [[1,1], [2,2], [3,3], [4,4], [5,5], [1,2], [2,3], [1,3], [1,4], [4,5], [1,5], [3,4]]
# )

# U = Set([1,2,3]) # Transitivity
# P = Set(
#     [[1,1],[2,2],[3,3],[2,3],[1,2]]
# )

U = Set([1,2,3])
P = Set([ # Anti_transitivity
    [1,2], [2,3]
])

# print(check_reflecsive(U, P))
# print(check_anti_reflecsive(U, P))
# print(check_symmetry(U, P))
# print(check_anti_symmetry(U, P))
# print(check_transitivity(U, P))
# print(check_anti_transitivity(U, P))

if __name__== "__main__":
    U = Set([1, 2, 3, 4, 5])
    P = Set(
        [[1, 1],[1, 2],[2, 2],[2, 1],[1, 3],[1, 5],[2, 3],[3, 1],[3, 2],[3, 3],[4, 4],[5, 1],[5, 5],[5, 3],[5, 4]]
    )

    # U = Set([1,2,3])
    # P = Set([[1,1],[2,2],[3,3],[1,2],[2,1]])

    print(*generate_matrix(U, P), sep="\n", end="\n\n")

    is_reflecsive = check_reflecsive(U, P)
    is_antireflecsive = check_anti_reflecsive(U, P)
    is_symmetric = check_symmetry(U, P)
    is_antisymmetric = check_anti_symmetry(U, P)
    is_transitive = check_transitivity(U, P)
    is_antitransitive = check_anti_transitivity(U, P)

    if is_reflecsive:
        print("Reflecsive")
    elif is_antitransitive:
        print("Anti-Reflecsive")
    elif is_reflecsive == False and is_antireflecsive == False:
        print("Neither Reflecsive nor Anti-Reflecsive")

    if is_symmetric:
        print("Symmetric")
    elif is_antisymmetric:
        print("Anti-Symmetric")
    elif is_antisymmetric == False and is_symmetric == False:
        print("Neither Symmetric nor Anti-Symmetric")

    if is_transitive:
        print("Transitive")
    elif is_antitransitive:
        print("Anti-Transitive")
    elif is_antitransitive == False and is_transitive == False:
        print("Neither Transitive nor Anti-Transitive")