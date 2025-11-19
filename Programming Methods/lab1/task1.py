import re

# line = input()
line = "123 1234 143 51437 aboba 153 53 15 15 3"
res = re.findall(r"\b1[245]3\b", line)

print(res)