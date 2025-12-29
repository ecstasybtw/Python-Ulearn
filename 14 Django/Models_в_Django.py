from django.db import models


class SiteUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_name()

    class Meta:
        db_table = 'site_users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Vacancy(models.Model):
    name = models.TextField()
    salary = models.FloatField()
    area_name = models.TextField()
    published_at = models.TextField()

    class Meta:
        db_table = 'vacancies'
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
