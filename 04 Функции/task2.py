from task1 import *

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
            salary_string = f'{vacancy['salary_from']} - {vacancy['salary_to']} {(vacancy['salary_currency'])} {(vacancy['salary_gross'])}'
            formatted['Оклад'] = salary_string
            continue
        if title in ['salary_to', 'salary_currency', 'salary_gross']:
            continue
        formatted[translate_title(title)] = value    
            
    return formatted
