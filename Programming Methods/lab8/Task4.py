from typing import List
import csv

def retrieve_data() -> List[tuple]:
    with open("./Task4.csv") as file:
        return [tuple(map(str.strip, line.split(","))) for line in file.read().split("\n")]
    
def form_info(data: List[tuple]) -> dict:
    result = dict()
    for line in data:
        owner = " ".join([line[2], line[3]])
        if not(result.get(owner)):
            result[owner] = [(line[0], line[1])]
        else:
            result[owner] += [(line[0], line[1])]
    return result

def pprint(data: dict):
    for k, v in data.items():
        print(f"{k}: ")
        for line in v:
            print(f"\tКличка: {line[0]}, Возраст: {line[1]}")

def main():
    data = retrieve_data()
    info = form_info(data)
    pprint(info)

if __name__ == "__main__":
    main()