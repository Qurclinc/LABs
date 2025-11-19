from typing import Iterable
from Task3 import timer

@timer
def my_join(delimiter: str, iterable: Iterable) -> str:
    result = ""
    for el in iterable:
        result += delimiter + str(el)
    return result.lstrip(delimiter)

@timer
def test_join(delimiter: str, iterable: Iterable):
    return delimiter.join(iterable) 

def main():
    lst = ["aboba", "xd", "lol"] * 1000
    my_join("+", lst)
    test_join("+", lst)

    
if __name__ == "__main__":
    main()