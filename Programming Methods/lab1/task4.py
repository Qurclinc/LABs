import re

# line = input()
line = "123 1234 143 51437 aboba 153 53 15 15 3 a ab abo aboba ab0ba"
res = re.findall(r"\b[A-Za-zА-Яа-яЁё]+\b", line)

print(res)