from django.db import models


class Score(models.Model):
    job_status_score = models.PositiveIntegerField(null=True, blank=True)
    language_score = models.PositiveIntegerField(null=True, blank=True)
    prof_exp_score = models.PositiveIntegerField(null=True, blank=True)
    education_score = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        profile_obj = self.profile_set.first()
        profile_obj.total_score = self.job_status_score + self.language_score + \
                                self.prof_exp_score + self.education_score
        profile_obj.save()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'JS:{self.job_status_score} L:{self.language_score} PE:{self.prof_exp_score} E:{self.education_score}'

