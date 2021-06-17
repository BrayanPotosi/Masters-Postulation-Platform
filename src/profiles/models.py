from django.db import models

# Create your models here.


class JobStatus(models.Model):
    has_job = models.BooleanField(default=False, null=False)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    change_opt = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company_name}, {self.salary}'


class ProfessionalExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile}, {self.company_name}'


class Languages(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    language = models.CharField(max_length=25, unique=True)
    level = models.ForeignKey(CambridgeLevel, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile}, {self.language}'


class Countries(models.Model):
    country_name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.country_name}'


class Cities(models.Model):
    city_name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.city_name}'


class Address(models.Model):
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=20)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.postal_code}, {self.city}, {self.country}'


class AdminLog(models.Model):
    admin = models.ForeignKey(Users,  on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.admin}, {self.device}, {self.count}'


class CandidateLog(models.Model):
    candidate = models.ForeignKey(Users, on_delete=models.SET_NULL)
    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    device = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.candidate}, {self.device}'


class CambridgeLevel(models.Model):
    level = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.level}'