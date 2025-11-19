import re


def main():
    # word = input("Enter line: ")
    word = "a123bc34d8ef34"
    # word = "leet1234code234"
    # word = "a1b01c001"
    print(len(set([int(x) for x in re.split(r"[a-z]", word) if x])))
    
    # Однострочное решение
    # print(len(set([int(x) for x in __import__("re").split(r"[a-z]", input("Enter line: ")) if x])))
    
    
if __name__ == "__main__":
    main()