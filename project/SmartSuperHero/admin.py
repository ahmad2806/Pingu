from django.contrib import admin
from SmartSuperHero.models import Doctor, Patient, GenericQuestion, Question, Report

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(GenericQuestion)
admin.site.register(Question)
admin.site.register(Report)