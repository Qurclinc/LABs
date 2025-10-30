def define_odds_numbers(N: int) -> bool:
    while N != 0:
        if (N % 10) % 2 != 0:
            return True
        N //= 10
    return False

def main():
    N = int(input("N = "))
    if N <= 0:
        print("N > 0!!!")
        return
    res = define_odds_numbers(N)
    print(res)

if __name__ == "__main__":
    main()