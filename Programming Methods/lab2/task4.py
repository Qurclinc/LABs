import re

# text = input()
text = "Lorem1 ipsum 11 dolor1337 sit56, 56 amet 78 consectetur 56adipisicing elit. Totam78, 7878 magni nemo? Tempora minima voluptate maiores dolore, beatae assumenda dicta eveniet, veritatis explicabo odio illum? Fugiat suscipit accusamus deleniti aperiam magnam."
pattern = r"\b(?P<word1>[A-Za-z]+)\d+[A-Za-z]*|\d+(?P<word2>[A-Za-z]+)"

# def clean_word(match):
#    return re.sub(r"\d+", "", match.group(0))

# result = re.sub(pattern, clean_word, text)
result = re.sub(pattern, lambda m: m.group("word1") or m.group("word2"), text)

print(result)
