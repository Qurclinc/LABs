import re

text = "Lorem1 ipsum 11 dolor1337 sit56, 56 amet 78 consectetur adipisicing elit. Totam78, 7878 magni nemo? Tempora minima voluptate maiores dolore, beatae assumenda dicta eveniet, veritatis explicabo odio illum? Fugiat suscipit accusamus deleniti aperiam magnam."
pattern = r"(\b[A-Za-z]+)(\d+)"
result = re.sub(pattern, lambda match: match.group(1), text)

print(result)