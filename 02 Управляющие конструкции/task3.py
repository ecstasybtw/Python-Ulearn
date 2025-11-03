from math import floor
from task2 import *
from collections import Counter, defaultdict


def declension(value: int, one, few, many) -> str:
    if 11 <= value % 100 <= 14:
        return many
    else:
        if value % 10 == 1:
            return one
        elif 2 <= value % 10 <= 4:
            return few
        else:
            return many

def find_available(normalized):
    total = [available for available in normalized if available.get('salary_currency') == 'RUR']
    return total

def find_highest_salary(available):
    salary = []
    for rec in available:
        try:
            avg = (float(rec.get('salary_to')) + float(rec.get('salary_from'))) / 2
        except (TypeError, ValueError):
            if rec.get("salary_to") == "Нет данных":
                avg = int(float(rec.get("salary_from")) // 2)
            elif rec.get("salary_from") == "Нет данных":
                avg = int(float(rec.get("salary_to")) // 2)

        name = rec.get('name')
        employer = rec.get('employer_name')
        city = rec.get('area_name')
        salary.append((avg, name, employer, city))

    sorted_salary = sorted(salary, key=lambda x: x[0], reverse=True)[:10]
    return sorted_salary


def find_lowest_salary(available):
    salary = []
    for rec in available:
        try:
            avg = int((float(rec.get('salary_to')) + float(rec.get('salary_from')))) / 2
        except (TypeError, ValueError):
            if rec.get("salary_to") == "Нет данных":
                avg = int(float(rec.get("salary_from")) // 2)
            elif rec.get("salary_from") == "Нет данных":
                avg = int(float(rec.get("salary_to")) // 2)

        name = rec.get('name')
        employer = rec.get('employer_name')
        city = rec.get('area_name')
        salary.append((avg, name, employer, city))

    sorted_salary = sorted(salary, key=lambda x: x[0])[:10]
    return sorted_salary

def find_popular_skills(available):
    skills_count = Counter()
    for rec in available:
        skill = rec.get('key_skills')
        if not skill:
            continue
        tokens = list(dict.fromkeys(token.strip() for token in skill.split(';') if token.strip()))
        if tokens:
            skills_count.update(tokens)

    skills = list(skills_count.keys())
    skills.sort(key=skills_count.get, reverse=True)
    top = [(s, skills_count[s]) for s in skills[:min(10, len(skills_count))]]
    return top, len(skills_count)

def find_city_avg_salaries(available):
    sums = defaultdict(float)
    counts = defaultdict(int)
    for rec in available:
        city = rec['area_name']
        try:
            lo = float(rec['salary_from'])
            hi = float(rec['salary_to'])
            avg = (lo + hi) // 2
        except (TypeError, ValueError):
            if rec.get("salary_to") == "Нет данных":
                avg = int(float(rec.get("salary_from")) // 2)
            elif rec.get("salary_from") == "Нет данных":
                avg = int(float(rec.get("salary_to")) // 2)

        sums[city] += avg
        counts[city] += 1

    threshold = len(available) // 100
    result = [(city, floor(sums[city] / cnt), cnt) for city, cnt in counts.items() if cnt >= threshold]
    result.sort(key=lambda x: x[1], reverse=True)

    return (result[:min(10, len(result))], len(result))

def print_info(available):
    best = []
    worst = []
    skills_top = []
    total_skills = 0
    city_stats = []
    total_cities = 0
    amount = 0
    rub = ""
    times_word = ""
    vac_word = ""
    skills_word = ""
    cities_word = ""

    best = find_highest_salary(available)
    worst = find_lowest_salary(available)
    skills_top, total_skills = find_popular_skills(available)
    city_stats, total_cities = find_city_avg_salaries(available)

    print("Самые высокие зарплаты:")
    for i, (avg, name, employer, city) in enumerate(best):
        amount = int(floor(avg))
        rub = declension(amount, "рубль", "рубля", "рублей")
        print(f'    {i + 1}) {name} в компании "{employer}" - {amount} {rub} (г. {city})')
    print()

    print("Самые низкие зарплаты:")
    for i, (avg, name, employer, city) in enumerate(worst):
        amount = int(floor(avg))
        rub = declension(amount, "рубль", "рубля", "рублей")
        print(f'    {i + 1}) {name} в компании "{employer}" - {amount} {rub} (г. {city})')
    print()

    skills_word = declension(total_skills, "скилл", "скилла", "скиллов")
    print(f"Из {total_skills} {skills_word}, самыми популярными являются:")
    for i, (skill, cnt) in enumerate(skills_top):
        times_word = declension(cnt, "раз", "раза", "раз")
        print(f"    {i + 1}) {skill} - упоминается {cnt} {times_word}")
    print()

    cities = [row["area_name"] for row in available]
    cities_word = declension(total_cities, "города", "городов", "городов")
    print(f"Из {len(set(cities))} {cities_word}, самые высокие средние ЗП:")
    for i, (city, avg_floor, cnt) in enumerate(city_stats):
        rub = declension(avg_floor, "рубль", "рубля", "рублей")
        vac_word = declension(cnt, "вакансия", "вакансии", "вакансий")
        print(f"    {i + 1}) {city} - средняя зарплата {avg_floor} {rub} ({cnt} {vac_word})")


def main():
    available = find_available(parse_csv())
    print_info(available)


if __name__ == '__main__':
    main()
