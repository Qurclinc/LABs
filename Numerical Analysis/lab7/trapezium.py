from typing import List
from general import rectangle_print_line, f

def find_integ_sum(h: float, results: List[float]):
    return (h / 2) * (float(results[0]) + float(results[-1]) + 2 * sum(map(float, results[1:-1])))

def make_tab(n: int, start: int, stop: int, number: int):
    h = 1 / n
    i = 0
    results = []
    while i <= n:
        res = f(start)
        rectangle_print_line(i, start, res)
        start = round(start + h, 2)
        results.append(f"{res:.6f}")
        i += 1
    print(f"I{number} = ({h} / 2) ({results[0]} + {results[-1]} + 2*({' + '.join(results[1:-1])}) = {find_integ_sum(h, results):.6f}")

if __name__ == "__main__":
    make_tab(10, 3, 4, number=1)
    print("\n\n\n")
    make_tab(20, 3, 4, number=2)