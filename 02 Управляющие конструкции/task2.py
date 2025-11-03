import csv
import html
import re

def normalize_html(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_cell(value):
    if not value.strip():
        return 'Нет данных'

    parts = [normalize_html(part) for part in value.split('\n') if part.strip()]
    return '; '.join(parts) if parts else 'Нет данных'

def parse_csv():
    with open('vacancies_for_learn_demo.csv', 'r', encoding='utf-8-sig', newline='') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        normalized = []

        for lines in csv_reader:
            if sum([1 for cell in lines if cell]) * 2 >= len(headers):
                record = {}
                for index, line in enumerate(lines):
                    record[headers[index]] = normalize_cell(line)
                normalized.append(record)
    return normalized
