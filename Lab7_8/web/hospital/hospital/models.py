from django.contrib.auth.models import User
from django.db import models

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    prof = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.prof})"


class ReasonForVisit(models.Model):
    reason_id = models.AutoField(primary_key=True)
    reason_name = models.CharField(max_length=200)

    def __str__(self):
        return self.reason_name


class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonForVisit, on_delete=models.CASCADE)
    duration = models.IntegerField()

    def __str__(self):
        return f"Посещение {self.patient} у {self.doctor} {self.duration}"

class MedicalCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bload = models.CharField(max_length=200)

    def __str__(self):
        return f"Группа крови пациента {self.patient} : {self.bload}"



class Study(models.Model):
    study_id = models.AutoField(primary_key=True)
    study_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.study_name

class PatientStudy(models.Model):
    patientstudy_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    date_performed = models.DateField(null=True, blank=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Исследование {self.study} для {self.patient}"