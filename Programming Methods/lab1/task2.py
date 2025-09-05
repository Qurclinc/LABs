import re

# line = input()
line = "a*b a**boba a**********b a****b****a***b aboba"
res = re.findall(r"\ba\**b\b", line)

print(res)