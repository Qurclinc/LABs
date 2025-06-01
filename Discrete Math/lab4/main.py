def solve():
    print("x\ty\tz\tF")
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                F = (x or (not(y)) or z) and ((not(x)) and (not(y)) and (not(z)))
                print(f"{x}\t{y}\t{z}\t{int(F)}")

if __name__ == "__main__":
    solve()