from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count, F
from django.db.models.functions import Substr, Round
from django.shortcuts import render, get_object_or_404
from .models import SiteUser, Vacancy


@csrf_exempt
def hello(request):
    input_user_id = request.POST.get('id', '') if request.method == 'POST' else ''
    display_name = "пользователь"
    if input_user_id:
        user_instance = get_object_or_404(SiteUser, id=input_user_id)
        display_name = user_instance.get_name()
    return render(request, 'hello.html', {'name': display_name})


def all_vacancies(request):
    vacancy_list = Vacancy.objects.all()
    table_data = [
        {
            'name': v.name,
            'salary': v.salary,
            'area_name': v.area_name,
            'published_at': v.published_at
        }
        for v in vacancy_list
    ]
    return render(request, 'vacancies_table.html', {'data': table_data})


def filter_vacancies(request):
    name_prefix = request.GET.get('name_start', '')
    min_salary = request.GET.get('salary', '')
    city_prefix = request.GET.get('city_start', '')

    query_set = Vacancy.objects.all()

    if name_prefix:
        query_set = query_set.filter(name__startswith=name_prefix)
    if min_salary.isdigit():
        query_set = query_set.filter(salary__gte=int(min_salary))
    if city_prefix:
        query_set = query_set.filter(area_name__startswith=city_prefix)

    filtered_data = [
        {
            'name': v.name,
            'salary': v.salary,
            'area_name': v.area_name,
            'published_at': v.published_at
        }
        for v in query_set
    ]
    return render(request, 'vacancies_table.html', {'data': filtered_data})


def get_salary_year_dynamic(request):
    yearly_salary_stats = (
        Vacancy.objects
        .annotate(year=Substr('published_at', 1, 4))
        .values('year')
        .annotate(salary=Round(Avg('salary')))
        .order_by('year')
    )
    chart_data = [
        {'first': str(item['salary']), 'second': str(item['year'])}
        for item in yearly_salary_stats
    ]
    return render(
        request,
        'dynamics_table.html',
        {
            'first_parameter': 'Avg salary',
            'second_parameter': 'Year',
            'data': chart_data
        }
    )


def get_count_year_dynamic(request):
    yearly_counts = (
        Vacancy.objects
        .filter(salary__isnull=False)
        .annotate(year=Substr('published_at', 1, 4))
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    chart_data = [
        {'first': str(item['count']), 'second': str(item['year'])}
        for item in yearly_counts
    ]
    return render(
        request,
        'dynamics_table.html',
        {
            'first_parameter': 'Vacancies count',
            'second_parameter': 'Year',
            'data': chart_data
        }
    )


def get_top_10_salary_city(request):
    total_vacancy_count = Vacancy.objects.filter(salary__isnull=False).count()

    city_salary_info = (
        Vacancy.objects
        .filter(salary__isnull=False)
        .values('area_name')
        .annotate(
            count=Count('salary'),
            a_salary=Round(Avg('salary'), 2),
            percentage=F('count') * 100.0 / total_vacancy_count
        )
        .filter(percentage__gt=1)
        .order_by('a_salary')[:10]
    )
    top_cities_list = [
        {'first': str(item['a_salary']), 'second': str(item['area_name'])}
        for item in city_salary_info
    ]
    return render(
        request,
        'dynamics_table.html',
        {
            'first_parameter': 'Avg salary',
            'second_parameter': 'City',
            'data': top_cities_list
        }
    )


def get_top_10_vac_city(request):
    total_vacancy_count = Vacancy.objects.filter(salary__isnull=False).count()

    city_vacancy_info = (
        Vacancy.objects
        .filter(salary__isnull=False)
        .values('area_name')
        .annotate(
            count=Count('salary'),
            percentage=Round(F('count') * 1.0 / total_vacancy_count, 4)
        )
        .filter(percentage__gt=0.01)
        .order_by('-percentage')[:10]
    )
    top_city_vacancies = [
        {'first': str(item['percentage']), 'second': str(item['area_name'])}
        for item in city_vacancy_info
    ]
    return render(
        request,
        'dynamics_table.html',
        {
            'first_parameter': 'Vacancy rate',
            'second_parameter': 'City',
            'data': top_city_vacancies
        }
    )
