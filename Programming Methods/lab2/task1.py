import re

# lines = input().split()
lines = ["#DEADBE", "XD", "XD#129123", "#fe12de", "*88*", "#129123XD", "*888*", "+-----+"]

pattern = r"^#[0-9a-fA-F]{6}$"
for line in lines:
    print(("Yes" if re.match(pattern, line) else "No") + "\t" + line)
