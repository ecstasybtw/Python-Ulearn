import csv

file_name = input()
lines = []
with open(file_name, 'r', encoding='utf-8-sig', newline='') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)
    for line in csv_reader:
        filled = []
        for value in line:
            value = value.strip()
            filled.append(value)
        if (len(filled) - filled.count('')) * 2 >= len(headers):
            lines.append(line)

print(headers)
print(lines)
