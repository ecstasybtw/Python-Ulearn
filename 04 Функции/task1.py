import csv
from prettytable import PrettyTable, ALL

def csv_reader(file_name):
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        titles = reader.fieldnames
        vacancies = list(reader)

    return titles, vacancies

def translate_title(title):
    translation = {
        'name': 'Название',
        'description': 'Описание',
        'key_skills': 'Навыки',
        'experience_id': 'Опыт работы',
        'premium': 'Премиум-вакансия',
        'employer_name': 'Компания',
        'salary_from': 'Нижняя граница вилки оклада',
        'salary_to': 'Верхняя граница вилки оклада',
        'salary_gross': 'Оклад указан до вычета налогов',
        'salary_currency': 'Идентификатор валюты оклада',
        'area_name': 'Название региона',
        'published_at': 'Дата публикации вакансии'
    }

    if title in translation:
        title = translation[title]

    return title

def translate_experience(exp):
    translation = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"
        }

    if exp in translation:
        exp = translation[exp]

    return exp

def translate_currency(currency):
    translation = {
        "AZN": "Манаты",
        "BYR": "Белорусские рубли",
        "EUR": "Евро",
        "GEL": "Грузинский лари",
        "KGS": "Киргизский сом",
        "KZT": "Тенге",
        "RUR": "Рубли",
        "UAH": "Гривны",
        "USD": "Доллары",
        "UZS": "Узбекский сум"
    }

    if currency in translation:
        currency = translation[currency]

    return currency

def formatter(vacancy):
    formatted = {}
    for title in vacancy:
        value = vacancy[title]
        value = value.strip()
        if value == 'False':
            value = 'Нет'
        elif value == 'True':
            value = 'Да'
        if title == 'key_skills':
            value = value.replace('\n', ', ')
        elif title == 'experience_id':
            value = translate_experience(value)
        elif title == 'salary_currency':
            value = translate_currency(value)
        if title == 'salary_from':
            salary_from = float(vacancy['salary_from'])
            salary_to = float(vacancy['salary_to'])
            salary_from_fmt = f"{int(salary_from):,}".replace(",", " ")
            salary_to_fmt = f"{int(salary_to):,}".replace(",", " ")
            currency = translate_currency(vacancy['salary_currency'])
            gross = 'Без вычета налогов' if vacancy['salary_gross'] == 'True' else 'С вычетом налогов'
            salary_string = f"{salary_from_fmt} - {salary_to_fmt} ({currency}) ({gross})"
            formatted['Оклад'] = salary_string
            continue
        if title in ['salary_to', 'salary_currency', 'salary_gross']:
            continue
        if len(value) > 100:
            value = value[:100] + '...'
        formatted[translate_title(title)] = value

    return formatted


def print_vacancies(vacancies, titles):
    if not vacancies:
        print("Нет данных")
        return

    translated_titles = []
    for title in titles:
        if title == 'salary_from':
            translated_titles.append('Оклад')
        elif title in ['salary_to', 'salary_currency', 'salary_gross']:
            continue
        else:
            translated_titles.append(translate_title(title))

    table = PrettyTable()
    table.hrules = ALL
    table.vrules = ALL
    table.field_names = ["№"] + translated_titles
    for col in table.field_names:
        table.max_width[col] = 20
    table.align = "l"

    for index, vacancy in enumerate(vacancies, start=1):
        formatted = formatter(vacancy)
        row = [index]
        for t in translated_titles:
            row.append(formatted.get(t, ""))
        table.add_row(row)


    print(table)

def main():
    file = input()
    titles, vacancies = csv_reader(file)
    print_vacancies(vacancies, titles)

if __name__ == '__main__':
    main()
