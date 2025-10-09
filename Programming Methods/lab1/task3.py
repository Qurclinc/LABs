import re

# line = input()
line = "123aboa456 148a471 123a678d 3a3"
res = re.findall(r"\b3[A-Za-zА-Яа-яЁё]3\b", line)

print(res)