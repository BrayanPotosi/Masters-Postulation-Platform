from django.contrib import admin
from .models import AdminLog, CandidateLog

admin.site.register(AdminLog)
admin.site.register(CandidateLog)


