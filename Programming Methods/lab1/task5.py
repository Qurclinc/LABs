import re

# line = input()
line = "+00000+ +0+ +00+ +1+1 *88* *** *888* +-----+"
#res = re.findall(r"(\s\+[0-]*\+\s)|(\s\*[8-]*\*\s)", line)
res = re.findall(r"(?<!\S)\+[0-]*\+(?!\S)|(?<!\S)\*[8-]*\*(?!\S)", line)

print(res)