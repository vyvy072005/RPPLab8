from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor, ReasonForVisit, Visit, Study, PatientStudy

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(ReasonForVisit)
admin.site.register(Visit)
admin.site.register(Study)
admin.site.register(PatientStudy)