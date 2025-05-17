from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient  # Импортируйте вашу модель
from .forms import PatientForm  # Создадим эту форму позже



def home_view(request):
    return render(request, 'hospital/templates/patient_list.html') # Замените 'hospital/home.html' на имя вашего шаблона

def patient_list(request):
    """Отображает список всех пациентов."""
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, pk):
    """Отображает детали одного пациента."""
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'myapp/patient_detail.html', {'patient': patient})

def patient_create(request):
    """Создает нового пациента."""
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_detail', pk=patient.pk)  # Перенаправляем на страницу деталей
    else:
        form = PatientForm()
    return render(request, 'myapp/patient_edit.html', {'form': form})

def patient_update(request, pk):
    """Редактирует существующего пациента."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'myapp/patient_edit.html', {'form': form})

def patient_delete(request, pk):
    """Удаляет пациента."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')  # Перенаправляем на список
    return render(request, 'myapp/patient_delete.html', {'patient': patient})