# Django
from django.contrib import admin

# Models
from .models import AdminLog, CandidateLog, AgeWeight, ExperienceWeight, HasJobWeight

admin.site.register(AdminLog)
admin.site.register(CandidateLog)
admin.site.register(AgeWeight)
admin.site.register(ExperienceWeight)
admin.site.register(HasJobWeight)
