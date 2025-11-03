vacation = input('Введите название вакансии: ')
discription = input('Введите описание вакансии: ')
city = input('Введите город для вакансии: ')
experience = int(input('Введите требуемый опыт работы (лет): '))
min_sal = int(input('Введите нижнюю границу оклада вакансии: '))
max_sal = int(input('Введите верхнюю границу оклада вакансии: '))
free_schedule = input("Нужен свободный график (да / нет): ")
free_schedule = free_schedule.lower() == "да"
premium = input("Является ли данная вакансия премиум-вакансией (да / нет): ")
premium = premium.lower() == "да"

data = [vacation, discription, city, experience, min_sal, max_sal, free_schedule, premium]

for value in data:
    print(f"{value} ({type(value).__name__})")
