from django.contrib import admin
from .models import (
    CivilStatus,
    JobStatus,
    Countries,
    Cities,
    Address,
    Profile,
    LastGrade,
    GottenGrade,
    Education,
    ProfessionalExperience,
    CambridgeLevel,
    Languages,
)

admin.site.register(CivilStatus)
admin.site.register(JobStatus)
admin.site.register(Countries)
admin.site.register(Cities)
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(LastGrade)
admin.site.register(Education)
admin.site.register(GottenGrade)
admin.site.register(ProfessionalExperience)
admin.site.register(CambridgeLevel)
admin.site.register(Languages)