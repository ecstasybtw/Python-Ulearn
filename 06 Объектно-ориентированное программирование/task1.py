import csv
from var_dump import var_dump


def csv_reader(file_name):
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        titles = reader.fieldnames
        vacancies = list(reader)

    return titles, vacancies


class Vacancy:
    def __init__(self, vacancy, salary_obj):
        self.name = vacancy.get('name', '')
        self.description = vacancy.get('description', '')
        self.key_skills = vacancy.get('key_skills', '')
        self.experience_id = vacancy.get('experience_id', '')
        self.premium = vacancy.get('premium', '')
        self.employer_name = vacancy.get('employer_name', '')
        self.salary = salary_obj
        self.area_name = vacancy.get('area_name', '')
        self.published_at = vacancy.get('published_at', '')


class Salary:
    def __init__(self, vacancy):
        self.salary_from = vacancy.get('salary_from', '')
        self.salary_to = vacancy.get('salary_to', '')
        self.salary_gross = vacancy.get('salary_gross', '')
        self.salary_currency = vacancy.get('salary_currency', '')


def main():
    filename = input()
    titles, vacancies = csv_reader(filename)
    result_vacancies = []
    for vacancy in vacancies:
        salary_obj = Salary(vacancy)
        vacancy_obj = Vacancy(vacancy, salary_obj)
        result_vacancies.append(vacancy_obj)
    var_dump(result_vacancies)


if __name__ == '__main__':
    main()
