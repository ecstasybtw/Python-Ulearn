import csv
from datetime import datetime
from collections import defaultdict
import re


currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}


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

    def to_dict(self):
        data = {}
        for key, value in self.__dict__.items():
            if key == 'salary':
                for s_key, s_value in value.__dict__.items():
                    data[s_key] = s_value
            else:
                data[key] = value
        return data


class Salary:
    def __init__(self, vacancy):
        self.salary_from = vacancy.get('salary_from', '')
        self.salary_to = vacancy.get('salary_to', '')
        self.salary_gross = vacancy.get('salary_gross', '')
        self.salary_currency = vacancy.get('salary_currency', '')

    def get_average_salary(self):
        try:
            salary_from = float(self.salary_from) if self.salary_from else 0
            salary_to = float(self.salary_to) if self.salary_to else 0
        except ValueError:
            return 0

        if salary_from and salary_to:
            avg_salary = (salary_from + salary_to) / 2
        else:
            avg_salary = salary_from or salary_to

        rate = currency_to_rub.get(self.salary_currency, 1)
        return avg_salary * rate


class DataSet:
    def __init__(self, filename):
        self.filename = filename

    def csv_reader(self):
        with open(self.filename, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            titles = reader.fieldnames
            vacancies = list(reader)
        return titles, vacancies


class Statistics:
    def __init__(self, dataset):
        self.dataset = dataset

    def get_vacancies(self):
        titles, vacancies = self.dataset.csv_reader()
        result_vacancies = []
        for vacancy in vacancies:
            salary_obj = Salary(vacancy)
            vacancy_obj = Vacancy(vacancy, salary_obj)
            result_vacancies.append(vacancy_obj)
        self.vacancies = result_vacancies

    def get_years_avg_sal(self):
        result_dict = defaultdict(list)
        for vacancy in self.vacancies:
            year = int(re.search(r'\b\d{4}\b', vacancy.published_at).group())
            result_dict[year].append(vacancy.salary.get_average_salary())
        result = {year: round(sum(salaries) / len(salaries)) for year, salaries in result_dict.items()}
        return dict(sorted(result.items()))

    def get_years_vacancies(self):
        result_dict = defaultdict(int)
        for vacancy in self.vacancies:
            year = int(re.search(r'\b\d{4}\b', vacancy.published_at).group())
            if vacancy.name:
                result_dict[year] += 1
        return dict(sorted(result_dict.items()))

    def get_years_vacancy_avg_sal(self, profession_name):
        result_dict = defaultdict(list)
        for vacancy in self.vacancies:
            year = int(re.search(r'\b\d{4}\b', vacancy.published_at).group())
            if profession_name.lower() in vacancy.name.lower():
                result_dict[year].append(vacancy.salary.get_average_salary())
        result = {year: round(sum(salaries) / len(salaries)) for year, salaries in result_dict.items() if salaries}
        return dict(sorted(result.items()))

    def get_years_pf_vacancies(self, profession_name):
        result_dict = defaultdict(int)
        for vacancy in self.vacancies:
            year = int(re.search(r'\b\d{4}\b', vacancy.published_at).group())
            if profession_name.lower() in vacancy.name.lower():
                result_dict[year] += 1
        return dict(sorted(result_dict.items()))

    def get_city_avg_sal(self):
        result_dict = defaultdict(list)
        for vacancy in self.vacancies:
            result_dict[vacancy.area_name].append(vacancy.salary.get_average_salary())
        format_dict = {city: round(sum(salaries) / len(salaries)) for city, salaries in result_dict.items() if len(salaries) > 0}
        top_10 = dict(sorted(format_dict.items(), key=lambda x: x[1], reverse=True)[:10])
        return top_10

    def get_amount_city_vacancies(self):
        result_dict = defaultdict(int)
        for vacancy in self.vacancies:
            result_dict[vacancy.area_name] += 1
        format_dict = {city: round(count / len(self.vacancies), 4) for city, count in result_dict.items()}
        top_10 = dict(sorted(format_dict.items(), key=lambda x: x[1], reverse=True)[:10])
        return top_10

    def get_salary_stat(self, profession_name):
        self.get_vacancies()
        print(f"Средняя зарплата по годам: {self.get_years_avg_sal()}")
        print(f"Количество вакансий по годам: {self.get_years_vacancies()}")
        print(f"Средняя зарплата по годам для профессии '{profession_name}': {self.get_years_vacancy_avg_sal(profession_name)}")
        print(f"Количество вакансий по годам для профессии '{profession_name}': {self.get_years_pf_vacancies(profession_name)}")
        print(f"Средняя зарплата по городам: {self.get_city_avg_sal()}")
        print(f"Доля вакансий по городам: {self.get_amount_city_vacancies()}")


def main():
    filename = input()
    profession_name = input()
    dataset = DataSet(filename)
    statistics = Statistics(dataset)
    statistics.get_salary_stat(profession_name)


if __name__ == '__main__':
    main()
