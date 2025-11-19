import math

def find_distance(p1: tuple, p2: tuple) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def main():
    A = [(-2,1), (1,1), (5,2), (-1,1), (3,3)]
    N = len(A)
    max_distance = -1
    for i in range(N - 1):
        for j in range(i + 1, N):
            distance = find_distance(A[i], A[j])
            if distance > max_distance:
                p1, p2 = A[i], A[j]
                max_distance = distance
                
    print(f"Максимальное расстояние между точками: {p1} и {p2}")
    
if __name__ == "__main__":
    main()