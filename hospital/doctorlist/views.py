from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DoctorForm
from .models import Patient, Visit

from django.contrib.auth.decorators import login_required, user_passes_test

from patientlist.models import Doctor


