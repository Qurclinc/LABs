from general import rectangle_print_line, f

def make_tab(n: int, start: int, stop: int, number: int):
    h = 1 / n
    i = 0
    integ_sum = 0
    results = []
    while i <= n:
        res = f(start)
        rectangle_print_line(i, start, res)
        start = round(start + h, 2)
        if  1 <= i <= n:
            integ_sum += res
            results.append(f"{res:.6f}")
        i += 1
    integ_sum *= h
    print(f"I{number} = {h} ({' + '.join(results)}) = {integ_sum:.6f}")

if __name__ == "__main__":
    make_tab(10, 3, 4, number=1)
    print("\n\n\n")
    make_tab(20, 3, 4, number=2)