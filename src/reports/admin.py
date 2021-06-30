from django.contrib import admin
from .models import AdminLog, CandidateLog, AgeWeight, ExperinceWeight, HasJobWeight

admin.site.register(AdminLog)
admin.site.register(CandidateLog)
admin.site.register(AgeWeight)
admin.site.register(ExperinceWeight)
admin.site.register(HasJobWeight)
