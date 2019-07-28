import datetime

from django.db import models


# Create your models here.


class Doctor(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    license_id = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class Patient(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    patient_id = models.CharField(max_length=300)
    diagnosis = models.CharField(max_length=300)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, )
    birthday = models.CharField(max_length=100)
    parent_fullname = models.CharField(max_length=300)

    def __str__(self):
        return self.first_name


class GenericQuestion(models.Model):
    question = models.CharField(max_length=300)
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class Question(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=300)

    def __str__(self):
        return f"question: {self.question}  answer{self.answer}"


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_date = models.DateField(default=datetime.date.today)
    report_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"report for {self.patient.first_name} at {self.report_date}"
