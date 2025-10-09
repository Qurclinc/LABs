import re

# text = input()
text = "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Totam, magni nemo? Tempora minima voluptate maiores dolore, beatae assumenda dicta eveniet, veritatis explicabo odio illum? Fugiat suscipit accusamus deleniti aperiam magnam."
pattern = r"\b[a-z]\w*"
result = re.sub(pattern, lambda match: match.group().capitalize(), text)

print(result)
