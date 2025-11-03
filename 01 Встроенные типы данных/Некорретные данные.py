while True:
    vacancy = input('Введите название вакансии: ')
    if len(vacancy) == 0:
        print('Данные некорректны, повторите ввод')
    else:
        break

while True:
    description = input('Введите описание вакансии: ')
    if len(description) == 0:
        print('Данные некорректны, повторите ввод')
    else:
        break

city = input('Введите город для вакансии: ')

while True:
    try:
        experience = int(input('Введите требуемый опыт работы (лет): '))
        break
    except ValueError:
        print('Данные некорректны, повторите ввод')

while True:

    while True:
        try:
            min_sal = int(input('Введите нижнюю границу оклада вакансии: '))
            break
        except ValueError:
            print('Данные некорректны, повторите ввод')

    while True:
        try:
            max_sal = int(input('Введите верхнюю границу оклада вакансии: '))
            break
        except ValueError:
            print('Данные некорректны, повторите ввод')

    if min_sal <= max_sal:
        break
    else:
        print("Нижняя граница оклада должна быть не больше верхней границы. Повторите ввод.")


while True:
    answer = input("Нужен свободный график (да / нет): ")
    if answer.lower() in ("да", "нет"):
        free_schedule = answer
        break
    else:
        print('Данные некорректны, повторите ввод')

while True:
    answer = input("Является ли данная вакансия премиум-вакансией (да / нет): ")
    if answer.lower() in ('да', 'нет'):
        premium = answer
        break
    else:
        print('Данные некорректны, повторите ввод')

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
