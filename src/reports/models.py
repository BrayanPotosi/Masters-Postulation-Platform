# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class AdminLog(models.Model):
    admin = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.admin}, {self.device}, {self.count}'


class CandidateLog(models.Model):
    candidate = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.candidate}, {self.device}'


class HasJobWeight(models.Model):
    has_job = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.has_job}-{self.weight}'


class AgeWeight(models.Model):
    age_years_start = models.PositiveIntegerField(default=0)
    age_years_end = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.age_years_start} to {self.age_years_end}-{self.weight}'


class ExperienceWeight(models.Model):
    exp_months_start = models.PositiveIntegerField(default=0)
    exp_months_end = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.exp_months_start} to {self.exp_months_end}-{self.weight}'
