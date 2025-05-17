from django.urls import path
from django.views.generic import TemplateView

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('new_page/', views.my_new_page, name='my_new_page'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('doctor board/', views.doctor_dashboard, name='doctor_dashboard'),
    path('register/', views.register, name='register'),
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/update/', views.visit_update, name='visit_update'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('', TemplateView.as_view(template_name="index.html"), name='login'),



]