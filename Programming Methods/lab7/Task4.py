def main():
    A1, A2 = 1, 2
    N = int(input("N = "))
    if N <= 0:
        print("N должно быть больше 1")
        return
    if N == 1:
        print(A1)
    else:
        print(A1, A2, end=" ")
        K = 3
        while True:
            A3 = (A1 + 2 * A2) / 3
            print(A3, end=" ")
            A1, A2 = A2, A3
            if K == N:
                break
            K += 1

if __name__ == "__main__":
    main()