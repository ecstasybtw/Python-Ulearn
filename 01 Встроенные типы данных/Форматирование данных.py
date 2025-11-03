vacancy = input('Введите название вакансии: ')
description = input('Введите описание вакансии: ')
city = input('Введите город для вакансии: ')
experience = int(input('Введите требуемый опыт работы (лет): '))
min_sal = int(input('Введите нижнюю границу оклада вакансии: '))
max_sal = int(input('Введите верхнюю границу оклада вакансии: '))
free_schedule = input("Нужен свободный график (да / нет): ")
premium = input("Является ли данная вакансия премиум-вакансией (да / нет): ")

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

avg_sal = (min_sal + max_sal) // 2

print(f'{vacancy}')
print(f'Описание: {description}')
print(f'Город: {city}')
print(f"Требуемый опыт работы: {experience} {declension(experience, 'год', 'года', 'лет')}")
print(f"Средний оклад: {avg_sal} {declension(avg_sal, 'рубль', 'рубля', 'рублей')}")
print(f'Свободный график: {free_schedule.lower()}')
print(f'Премиум-вакансия: {premium.lower()}')
