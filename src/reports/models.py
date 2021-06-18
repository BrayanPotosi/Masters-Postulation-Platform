from django.db import models
from django.contrib.auth.models import User

class AdminLog(models.Model):
    admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.admin}, {self.device}, {self.count}'


class CandidateLog(models.Model):
    candidate = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.candidate}, {self.device}'