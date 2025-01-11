from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# Home page view
def home(request):
    return render(request, 'home.html')  

# Doctor login view
def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_doctor: 
                auth_login(request, user)
                return redirect('office:doctor_dashboard')  
            else:
                messages.error(request, "You do not have permission to log in as a doctor.")
        else:
            messages.error(request, "Invalid email or password for doctor.")
    return render(request, 'office:doctor_login.html')

# Doctor dashboard view
@login_required
def doctor_dashboard(request):
    return render(request, 'office/doctor_dashboard.html')

# Secretary login view
def secretary_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_secretary:  
                auth_login(request, user)
                return redirect('office:secretary_dashboard')  
            else:
                messages.error(request, "You do not have permission to log in as a secretary.")
        else:
            messages.error(request, "Invalid email or password for secretary.")
    return render(request, 'office:secretary_login.html')

# Secretary dashboard view
@login_required
def secretary_dashboard(request):
    return render(request, 'office/secretary_dashboard.html')



