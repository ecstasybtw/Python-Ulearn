import csv
from prettytable import PrettyTable, ALL


def csv_reader(file_name):
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        titles = reader.fieldnames
        vacancies = list(reader)

    return titles, vacancies


def range_detector(range_string):
    if range_string:
        parts = range_string.split()

        if not parts:
            return None, None
        start = int(parts[0]) if len(parts) > 0 else None
        end = int(parts[1]) if len(parts) > 1 else None

        return start, end
    return None, None


def formatter(vacancy):
    formatted = {}
    for title in vacancy:
        value = vacancy[title]
        value = value.strip()
        if len(value) > 100:
            value = value[:100] + '...'
        formatted[title] = value

    return formatted


def print_table(vacancies, titles, selected_titles=None, start=None, end=None):

    if start is not None:
        vacancies = vacancies[start - 1 :]
    if end is not None:
        vacancies = vacancies[: end - start + 1] if start else vacancies[:end]

    columns = (['№'] + selected_titles) if selected_titles else (['№'] + titles)

    table = PrettyTable()
    table.field_names = ['№'] + titles
    table.max_width = 20
    table.hrules = ALL
    table.align = "l"

    for i, vacancy in enumerate(vacancies, start=start or 1):
        formatted = formatter(vacancy)
        row = [i]
        for title in titles:
            value = formatted.get(title, '')
            row.append(value)
        table.add_row(row)

    print(table.get_string(fields=columns))


def main():
    file_name = input()
    selected_range = input()
    selected_titles = input()
    if not selected_titles:
        selected_titles = None
    else:
        selected_titles = [col.strip() for col in selected_titles.split(',')]

    titles, vacancies = csv_reader(file_name)
    start, end = range_detector(selected_range)
    print_table(vacancies, titles, selected_titles, start, end)


if __name__ == '__main__':
    main()
