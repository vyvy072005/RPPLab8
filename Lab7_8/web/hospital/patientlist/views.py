from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PatientForm, RegistrationForm, VisitForm, DoctorForm
from .models import Patient, Doctor, Visit

from django.contrib.auth.decorators import login_required, user_passes_test




def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin)
def doctor_list(request):
    doctor = Doctor.objects.all()
    #doctor = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctor})
@login_required
@user_passes_test(is_admin)
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor_detail.html', {'doctor': doctor})
@login_required
@user_passes_test(is_admin)
def doctor_create(request):
    """Создает нового пациента."""
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def doctor_update(request, pk):
    """Редактирует существующего пациента."""
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'doctor_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'patient_delete.html', {'doctor': doctor})

#------------------------------------------------------------------#
@login_required
@user_passes_test(is_doctor)
def visit_list(request):
    """Отображает список посещений для текущего врача."""
    try:
        doctor = Doctor.objects.get(doctor_id=request.user.id)
        visits = Visit.objects.filter(doctor=doctor)  # Фильтруем по врачу
        return render(request, 'visit_list.html', {'visits': visits})
    except Doctor.DoesNotExist:
        # Пользователь является врачом, но у него нет профиля врача
        return render(request, 'create_doctor_profile.html', {'message': 'Пожалуйста, создайте профиль врача, чтобы просматривать посещения.'})

# @login_required
# @user_passes_test(is_doctor)
# def visit_list(request):
#     """Отображает список посещений для текущего врача."""
#     #doctor = Doctor.objects.get(user=request.user)
#     visits = Visit.objects.all()
#     return render(request, 'visit_list.html', {'visits': visits})


# @login_required
# @user_passes_test(is_doctor)
# def visit_detail(request, pk):
#     """Отображает детали конкретного посещения."""
#     try:
#         doctor = Doctor.objects.get(doctor_id=request.user.id)
#         visit = get_object_or_404(Visit, pk=pk, doctor=doctor)  # Добавляем проверку врача
#         return render(request, 'doctor_detail.html', {'visit': visit})
#     except Doctor.DoesNotExist:
#         # Обработка ситуации, когда Doctor не существует
#         return render(request, 'login.html', {})  # Перенаправляем на страницу, предлагающую создать профиль врача
@login_required
@user_passes_test(is_doctor)
def visit_detail(request, pk):
    """Отображает детали конкретного посещения, принадлежащего врачу."""
    try:
        doctor = Doctor.objects.get(doctor_id=request.user.id)
        visit = get_object_or_404(Visit, pk=pk, doctor=doctor)  # Врач должен быть владельцем визита
        return render(request, 'visit_detail.html', {'visit': visit})
    except Doctor.DoesNotExist:
        # Пользователь является врачом, но у него нет профиля врача
        return render(request, 'create_doctor_profile.html', {'message': 'Пожалуйста, создайте профиль врача, чтобы просматривать посещения.'})  # Или другая страница с сообщением

@login_required
@user_passes_test(is_doctor)
@login_required
@user_passes_test(is_doctor)
def visit_create(request):
    """Создает новое посещение."""

    try:
        doctor = Doctor.objects.get(doctor_id=request.user.id)  # Получаем врача, используя doctor_id
    except Doctor.DoesNotExist:
        doctor = Doctor.objects.create(doctor_id=request.user.id, last_name="", first_name="", middle_name="", prof="")

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.doctor = doctor  # Автоматически заполняем врача
            visit.save()
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitForm()
    return render(request, 'doctor_form.html', {'form': form})


@login_required
@user_passes_test(is_doctor)
def visit_update(request, pk):
    """Редактирует существующее посещение."""
    try:
        doctor = Doctor.objects.get(doctor_id=request.user.id)
        visit = get_object_or_404(Visit, pk=pk, doctor=doctor)
    except Doctor.DoesNotExist:
        return render(request, 'doctor_profile_needed.html', {})

    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save()
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitForm(instance=visit)
    return render(request, 'doctor_form.html', {'form': form})


@login_required
@user_passes_test(is_doctor)
def visit_delete(request, pk):
    """Удаляет посещение."""
    try:
        doctor = Doctor.objects.get(doctor_id=request.user.id)
        visit = get_object_or_404(Visit, pk=pk, doctor=doctor)
    except Doctor.DoesNotExist:
        return render(request, 'doctor_profile_needed.html', {})

    if request.method == 'POST':
        visit.delete()
        return redirect('visit_list')
    return render(request, 'doctor_confirm_delete.html', {'visit': visit})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Проверка, является ли пользователь врачом
def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

@login_required  # Требуется аутентификация
@user_passes_test(is_doctor)  # Требуется, чтобы пользователь был в группе "Doctor"
def doctor_dashboard(request):
    """
    Представление для панели управления врача.
    Доступно только для аутентифицированных пользователей, состоящих в группе "Doctor".
    """
    context = {
        'message': 'Добро пожаловать, врач!',
    }
    return render(request, 'doctor_dashboard.html', context)

# Другие представления...
def home(request):
    # Пример представления, доступного всем
    return render(request, 'home.html')

def my_new_page(request):
    """Представление для новой страницы."""
    context = {
        'message': 'Привет, это моя новая страница!',
    }
    return render(request, 'my_new_page.html', context)

def patient_list(request):
    """Отображает список всех пациентов."""
    patients = Patient.objects.all()
    return render(request, 'patient_List.html', {'patients': patients})

def patient_detail(request, pk):
    """Отображает детали одного пациента."""
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_detail.html', {'patient': patient})

def patient_create(request):
    """Создает нового пациента."""
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patient_edit.html', {'form': form})

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
    return render(request, 'patient_edit.html', {'form': form})

def patient_delete(request, pk):
    """Удаляет пациента."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_delete.html', {'patient': patient})
