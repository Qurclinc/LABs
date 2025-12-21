from typing import List
from general import rectangle_print_line, f

def find_integ_sum(h: float, results: List[float]):
    results = list(map(float, results))
    # print(results, results[1::2], results[::2], sep="\n")
    return (h / 3) * (results[0] + results[-1] + 4 * sum(results[1:-1:2]) + 2 * sum(results[2:-1:2]))

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
    print(f"I{number} = ({h} / 3) ({results[0]} + {results[-1]} + 4*({' + '.join(results[1:-1:2])}) + 2*({' + '.join(results[2:-1:2])}) = {find_integ_sum(h, results):.6f}")

if __name__ == "__main__":
    make_tab(10, 3, 4, number=1)
    print("\n\n\n")
    make_tab(20, 3, 4, number=2)