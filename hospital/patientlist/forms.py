from django import forms
from django.contrib.auth.models import User

from .models import Patient, Doctor, Visit
from django.contrib.auth.forms import UserCreationForm
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # Или перечислите конкретные поля, которые хотите видеть в форме

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # Или перечислите конкретные поля


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['patient', 'duration', 'reason']  # Исключите doctor, его можно заполнить автоматически

class RegistrationForm(UserCreationForm):
     class Meta(UserCreationForm.Meta):
         model = User
         fields = UserCreationForm.Meta.fields # Добавьте поле email (если нужно)

