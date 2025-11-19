def table():
    SDNF, SKNF = [], []
    print("x\ty\tz\tF")
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                F = (x or (not(y)) or z) == ((not(x)) and (not(y)) and (not(z)))
                print(f"{x}\t{y}\t{z}\t{int(F)}")
                if F:
                    SDNF += [' '.join(["x" if x else "-x", "y" if y else "-y", "z" if z else "-z"])]
                else:
                    SKNF += [' '.join(["-x" if x else "x", "-y" if y else "y", "-z" if z else "z"])]
    print(f"SDNF= {SDNF}\nSKNF = {SKNF}")



if __name__ == "__main__":
    table()

