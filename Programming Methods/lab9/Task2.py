def is_happy(s: str, a: int, b: int, c: int) -> bool:
    return all(ch in ["a", "b", "c"] for ch in s) and \
            all(ch not in s for ch in ["aaa", "bbb", "ccc"]) and \
            s.count("a") == a and s.count("b") == b and s.count("c") == c
            
def build_happy_string(a: int, b: int, c: int) -> str | None:
    heap = [[a, "a"], [b, "b"], [c, "c"]]
    result = []
    while True:
        heap.sort(key=lambda x: x[0], reverse=True)
        char_to_add = None
        for i, (count, char) in enumerate(heap):    
            if count == 0:
                continue
            
            if len(result) >= 2 and result[-1] == char and result[-2] == char:
                continue
            char_to_add = i
            break
            
        if char_to_add is None:
            break
        
        count, char = heap[char_to_add]
        result.append(char)
        heap[char_to_add][0] = count - 1
        
    return "".join(result)

def main():
    # line = "abcaaba"
    a, b, c = 1, 1, 7
    line = build_happy_string(a, b, c)
    print(line)
    print(is_happy(line, a, b, c))
    
if __name__ == "__main__":
    main()