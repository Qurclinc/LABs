def find_side(c1, c2):
    return max(c1, c2) - min(c1, c2)

def main():
    x1, y1 = map(int, input("Enter (x1, y1): ").split())
    x2, y2 = map(int, input("Enter (x2, y2): ").split())
    width = find_side(x1, x2)
    height = find_side(y1, y2)
    
    S = width * height
    P = 2 * (width + height)
    
    print(f"Периметр: {P}\nПлощадь: {S}")
    
if __name__ == "__main__":
    main()
