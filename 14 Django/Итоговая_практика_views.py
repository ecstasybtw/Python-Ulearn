from django.db import IntegrityError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def add_user(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = int(request.POST['age'])
        email = request.POST['email']
        password = request.POST['password']
    except (KeyError, ValueError) as e:
        return render(request, 'error.html', {'error': 'Invalid or missing input data'})

    if not MyUser.verify_age(age):
        return render(request, 'error.html', {'error': 'Age must be greater than 18 and lower than 122!'})

    try:
        hashed_password = MyUser.hash_password(password)
        user = MyUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            password=hashed_password
        )
        return render(request, 'answer.html', {'answer': user.id})

    except IntegrityError:
        return render(request, 'error.html', {'error': 'User with this email already exists'})


@csrf_exempt
def delete_user(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return render(request, 'error.html', {'error': 'Email or password missing'})

    try:
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return render(request, 'error.html', {'error': 'User not found'})

    if not user.verify_password(password):
        return render(request, 'error.html', {'error': 'Wrong password'})

    user.delete()
    return render(request, 'answer.html', {'answer': True})


@csrf_exempt
def authorise(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return render(request, 'error.html', {'error': 'Email or password missing'})

    try:
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return render(request, 'error.html', {'error': 'User not found'})

    if not user.verify_password(password):
        return render(request, 'error.html', {'error': 'Wrong password'})

    return render(request, 'user_info.html', {'user': user,
                                              'skills': user.skills})

@csrf_exempt
def add_vacancy(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        name = request.POST['name']
        salary = int(request.POST['salary'])
        area_name = request.POST['area_name']

    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing input data'})

    vacancy = Vacancy.objects.create(
        name=name,
        salary=salary,
        area_name=area_name
    )

    return render(request, 'answer.html', {'answer': vacancy.id})

@csrf_exempt
def get_vacancy(request):
    if request.method != 'GET':
        return render(request, 'error.html', {'error': 'test vac'})

    try:
        vacancy_id = int(request.GET['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return render(request, 'error.html', {'error': 'Vacancy not found'})

    skills = vacancy.skills
    responses = UserResponse.objects.filter(vacancy=vacancy)

    return render(request, 'vacancy.html', {
        'vacancy': vacancy,
        'skills': skills,
        'responses': responses
    })


@csrf_exempt
def delete_vacancy(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        vacancy_id = int(request.POST['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy.delete()
        return render(request, 'answer.html', {'answer': True})
    except Vacancy.DoesNotExist:
        return render(request, 'error.html', {'error': 'Vacancy not found'})


@csrf_exempt
def add_skill(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        name = request.POST['name']
    except KeyError:
        return render(request, 'error.html', {'error': 'Name is required'})

    try:
        skill = Skill.objects.create(name=name)
        return render(request, 'answer.html', {'answer': skill.id})
    except IntegrityError:
        return render(request, 'error.html', {'error': 'Skill with this name already exists'})


@csrf_exempt
def get_skill(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        skill_id = int(request.POST['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        skill = Skill.objects.get(id=skill_id)
        return render(request, 'answer.html', {'answer': skill.name})
    except Skill.DoesNotExist:
        return render(request, 'error.html', {'error': 'Skill not found'})


@csrf_exempt
def delete_skill(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        skill_id = int(request.POST['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        skill = Skill.objects.get(id=skill_id)
        skill.delete()
        return render(request, 'answer.html', {'answer': True})
    except Skill.DoesNotExist:
        return render(request, 'error.html', {'error': 'Skill not found'})


@csrf_exempt
def get_all_skills(request):
    skills = Skill.objects.values_list('name', flat=True)
    answer = ", ".join(skills)
    return render(request, 'answer.html', {'answer': answer})


@csrf_exempt
def add_skill_to_vacancy(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        vacancy_id = int(request.POST['vacancy'])
        skill_id = int(request.POST['skill'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing vacancy/skill id'})

    try:
        VacancySkill.objects.create(vacancy_id=vacancy_id, skill_id=skill_id)
        return render(request, 'answer.html', {'answer': True})
    except IntegrityError:
        return render(request, 'error.html', {'error': 'Skill already linked to vacancy or invalid IDs'})


@csrf_exempt
def add_skill_to_user(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        user_id = int(request.POST['user'])
        skill_id = int(request.POST['skill'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing user/skill id'})

    try:
        UserSkill.objects.create(user_id=user_id, skill_id=skill_id)
        return render(request, 'answer.html', {'answer': True})
    except IntegrityError:
        return render(request, 'error.html', {'error': 'Skill already linked to user or invalid IDs'})


@csrf_exempt
def remove_skill_from_user(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        user_id = int(request.POST['user'])
        skill_id = int(request.POST['skill'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing user/skill id'})

    deleted_count, _ = UserSkill.objects.filter(user_id=user_id, skill_id=skill_id).delete()
    if deleted_count == 0:
        return render(request, 'error.html', {'error': 'Skill not found for user'})
    return render(request, 'answer.html', {'answer': True})


@csrf_exempt
def remove_skill_from_vacancy(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        vacancy_id = int(request.POST['vacancy'])
        skill_id = int(request.POST['skill'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing vacancy/skill id'})

    deleted_count, _ = VacancySkill.objects.filter(vacancy_id=vacancy_id, skill_id=skill_id).delete()
    if deleted_count == 0:
        return render(request, 'error.html', {'error': 'Skill not found for vacancy'})
    return render(request, 'answer.html', {'answer': True})


@csrf_exempt
def add_response(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        user_id = int(request.POST['user'])
        vacancy_id = int(request.POST['vacancy'])
        message = request.POST['message']
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing input data'})

    try:
        response = UserResponse.objects.create(
            user_id=user_id,
            vacancy_id=vacancy_id,
            message=message
        )
        return render(request, 'answer.html', {'answer': response.id})
    except IntegrityError:
        return render(request, 'error.html', {'error': 'Invalid user or vacancy ID'})


@csrf_exempt
def get_response(request):
    if request.method != 'GET':
        return render(request, 'error.html', {'error': 'Only GET allowed'})

    try:
        response_id = int(request.GET['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        response = UserResponse.objects.get(id=response_id)
        return render(request, 'answer.html', {'answer': response.message})
    except UserResponse.DoesNotExist:
        return render(request, 'error.html', {'error': 'Response not found'})


@csrf_exempt
def delete_response(request):
    if request.method != 'POST':
        return render(request, 'error.html', {'error': 'Only POST allowed'})

    try:
        response_id = int(request.POST['id'])
    except (KeyError, ValueError):
        return render(request, 'error.html', {'error': 'Invalid or missing id'})

    try:
        response = UserResponse.objects.get(id=response_id)
        response.delete()
        return render(request, 'answer.html', {'answer': True})
    except UserResponse.DoesNotExist:
        return render(request, 'error.html', {'error': 'Response not found'})
