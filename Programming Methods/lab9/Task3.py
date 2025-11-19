import json
import csv

def load_data() -> dict:
    result = {}
    with open("./users.json", "r") as f:
        data = json.loads(f.read())
    for line in data:
        if not(result.get(line["user"])):
            result[line["user"]] = {
                "activity": 0,
                "popularity": 0
            }
        if line["type"] == "лайк":
            result[line["user"]]["activity"] += 1
        elif line["type"] == "комментарий":
            result[line["user"]]["popularity"] += 1
    return result

def dump_data(data: dict):
    with open("./users.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        for k, v in data.items():
            writer.writerow([k, v["activity"], v["popularity"]])
            
def get_top_10(data: dict):
    top = {}
    for k, v in data.items():
        top[k] = v["activity"] + v["popularity"]
    print("Топ-10 активных: \n")
    print(*list(dict(sorted(top.items(), key=lambda x: x[1], reverse=True)[:10]).keys()), sep="\n")

def main():
    users = load_data()
    dump_data(users)
    get_top_10(users)

if __name__ == "__main__":
    main()