from django.db import models


class Score(models.Model):
    job_status_score = models.PositiveIntegerField(null=True, blank=True)
    language_score = models.PositiveIntegerField(null=True, blank=True)
    prof_exp_score = models.PositiveIntegerField(null=True, blank=True)
    education_score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'JS:{self.job_status_score} L:{self.language_score} PE:{self.prof_exp_score} E:{self.education_score}'

