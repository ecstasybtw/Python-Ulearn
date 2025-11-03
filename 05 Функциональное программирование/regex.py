import re
string = '70 000 - 150 000 (Рубли) (С вычетом налогов)'

pattern = re.compile(r'(\d[\d\s]*)\s*-\s*(\d[\d\s]*)\s*\(([^)]+)\)\s*\(([^)]+)\)')
result = pattern.search(string)
print(result.groups(0))
