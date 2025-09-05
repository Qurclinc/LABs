import re

# line = input()
line = "123aboa456 148a471 123a678d"
res = re.findall(r"\b\d{3}[A-Za-zА-Яа-яЁё]\d{3}\b", line)

print(res)