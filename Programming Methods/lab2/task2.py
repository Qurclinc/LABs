import re

# lines = input().split()
lines = ["Train-Case-Notation", "Not-train-Case", "Also- Not-Train", "and just wordss"]

pattern = r"^(?:[A-Z][a-z]*-?)+(?:[A-Z][a-z])?$"
for line in lines:
    print(("Yes" if re.match(pattern, line) else "No") + "\t" + line)
