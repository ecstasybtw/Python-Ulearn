import re

string = '1C: Бухгалтерия Программирование 1C: Учет SQL pandas'
block_pattern = re.compile(r'\S+:\s+\S+')
groups = block_pattern.finditer(string)
for group in groups:
    print(group.span())
print(groups)
