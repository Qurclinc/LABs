from Set import Set

A = Set([1, 2, 3, 4, 5])
B = Set([3, 4, 5, 6, 9, 10, 11, 12])
C = Set([5, 6, 7, 8, 9, 10, 13, 14])

P = Set.GetBoolean(A)

D1 = Set.Xor(A, B)

D2 = Set.Differ(C, Set.Unite(A, B))

D = Set.Product(D2, D1)

print(f"P(A) = {P}\n\nD1={D1}\n\nD2={D2}\n\nD={D}")