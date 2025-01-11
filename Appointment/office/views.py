from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import AppointmentForm 
from django.http import HttpResponse
from .forms import PrescriptionForm
from .models import Appointment, Prescription
from .forms import PatientForm, Patient
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from .forms import SecretaryForm,WorkingDayForm
from .models import Announcement,Secretary,WorkingDay


User = get_user_model()  


def home(request):
    return render(request, 'home.html')  

#LOGİN & LOGOUT

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user and user.is_doctor:
            auth_login(request, user)
            return redirect('office:doctor_dashboard')  
        else:
            messages.error(request, "Invalid credentials or no permission.")
    return render(request, 'doctor_login.html')

def doctor_logout(request):
    logout(request)
    return redirect('home') 

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)
    
    query = request.GET.get('q', '')  
    if query:
        appointments = Appointment.objects.filter(
            doctor=request.user,
            patient_name__icontains=query  
        ).order_by('appointment_date', 'appointment_time')
    else:
        appointments = Appointment.objects.filter(
            doctor=request.user
        ).order_by('appointment_date', 'appointment_time')
    
    patients = Patient.objects.all()  
    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'patients': patients
    })


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
    return render(request, 'secretary_login.html')

def secretary_logout(request):
    logout(request)
    return redirect('home')  

from .models import Announcement

def secretary_dashboard(request):
    secretaries = Secretary.objects.all()  
    announcements = Announcement.objects.order_by('-created_at')  
    prescriptions = Prescription.objects.order_by('-created_at')[:5]  
    working_days = WorkingDay.objects.all().order_by('-date')[:5] 

    context = {
        'secretaries': secretaries,
        'announcements': announcements,
        'prescriptions': prescriptions,
        'working_days': working_days,
    }
    return render(request, 'secretary_dashboard.html', context)

#APPOINTMENT 

@login_required
def list_appointments(request):
    if not request.user.is_secretary:
        return HttpResponse("Unauthorized", status=401)
    appointments = Appointment.objects.all()
    return render(request, 'list_appointment.html', {'appointments': appointments})

@login_required
def create_appointment(request):
    if not request.user.is_secretary:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            doctor = appointment.doctor
            appointment_date = appointment.appointment_date  
            appointment_time = appointment.appointment_time

            
            if not WorkingDay.objects.filter(date=appointment_date, doctor=doctor, status='Available').exists():
                messages.error(request, "The doctor is unavailable on the selected date. Please choose another date.")
            else:
                appointment.created_by = request.user
                appointment.save()
                messages.success(request, "Appointment successfully created!")
                return redirect('office:list_appointments')
    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form})
@login_required
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('office:list_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'update_appointment.html', {'form': form})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        next_url = request.POST.get('next', 'office:list_appointments') 
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect(next_url)
    return render(request, 'delete_appointment.html', {'appointment': appointment})


#PRESCRIPTION

@login_required
def list_prescriptions(request):
    prescriptions = Prescription.objects.filter(doctor=request.user)
    return render(request, 'list_prescriptions.html', {'prescriptions': prescriptions})

@login_required
def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.created_by = request.user

 
            prescription.save()
            return redirect('office:list_prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions_form.html', {'form': form})

@login_required
def update_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('office:list_prescriptions')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescriptions_form.html', {'form': form})

@login_required
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)
    if request.method == 'POST':
        prescription.delete()
        return redirect('office:list_prescriptions')
    return render(request, 'delete_prescription.html', {'prescription': prescription})


#PATİENT REGİSTER


@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient successfully added.')  
            return redirect('office:view_patients')
        else:
            messages.error(request, 'There was an error adding the patient.') 
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Patient information has been successfully updated.')
            return redirect('office:view_patients')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'update_patient.html', {'form': form, 'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()  
        messages.success(request, 'The patient has been successfully deleted.')
        return redirect('office:view_patients')
    return render(request, 'delete_patient.html', {'patient': patient})

def view_patients(request):
    patients = Patient.objects.all()  
    return render(request, 'view_patient.html', {'patients': patients})



#MEDICAL HISTORY
@login_required
def view_patient_medical_history(request, patient_id):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)

   
    patient = get_object_or_404(Patient, id=patient_id)

    
    medical_history_list = []
    if patient.medical_history:
        medical_history_list = patient.medical_history.split(',')

    return render(request, 'patient_medical_history.html', {
        'patient': patient,
        'medical_history_list': medical_history_list,
    })



#SECRETARY ADD

@login_required
def add_secretary(request):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)
    
    if request.method == 'POST':
        form = SecretaryForm(request.POST)
        if form.is_valid():
            secretary = form.save()
            
            Announcement.objects.create(message=f"New secretary {secretary.name} has been added to the {secretary.department} department.")
            messages.success(request, f"Secretary {secretary.name} has been added successfully.")
            return redirect('office:doctor_dashboard')
    else:
        form = SecretaryForm()
    
    return render(request, 'add_secretary.html', {'form': form})

@login_required
def list_secretaries(request):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)
    
    secretaries = Secretary.objects.all()
    return render(request, 'list_secretaries.html', {'secretaries': secretaries})

@login_required
def update_secretary(request, pk):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)
    
    secretary = get_object_or_404(Secretary, pk=pk)
    if request.method == 'POST':
        form = SecretaryForm(request.POST, instance=secretary)
        if form.is_valid():
            form.save()
            messages.success(request, "Secretary updated successfully!")
            return redirect('office:list_secretaries')
    else:
        form = SecretaryForm(instance=secretary)
    
    return render(request, 'update_secretary.html', {'form': form, 'secretary': secretary})
@login_required
def delete_secretary(request, pk):
    if not request.user.is_doctor:
        return HttpResponse("Unauthorized", status=401)
    
    secretary = get_object_or_404(Secretary, pk=pk)
    if request.method == 'POST':
        secretary.delete()
        messages.success(request, "Secretary deleted successfully!")
        return redirect('office:list_secretaries')
    
    return render(request, 'delete_secretary.html', {'secretary': secretary})





#WORKDAY
def manage_working_days(request):
    if request.method == "POST":
        form = WorkingDayForm(request.POST)
        if form.is_valid():
            working_day = form.save(commit=False)
            working_day.doctor = request.user  
            working_day.save()

           
            status_message = f"Doctor updated availability: {working_day.date} - {working_day.status}."
            Announcement.objects.create(message=status_message)

            return redirect('office:manage_working_days')

        
        if "clear_schedule" in request.POST:
            WorkingDay.objects.filter(doctor=request.user).delete()
            Announcement.objects.create(message="Doctor cleared the working schedule.")
            return redirect('office:manage_working_days')

    else:
        form = WorkingDayForm()

    working_days = WorkingDay.objects.filter(doctor=request.user).order_by('date')
    return render(request, 'manage_working_days.html', {
        'form': form,
        'working_days': working_days
    })

def clear_announcements(request):
    if request.method == 'POST':
        # Duyuruları temizle
        Announcement.objects.all().delete()
        # Reçeteleri temizle
        Prescription.objects.all().delete()
        return redirect('office:secretary_dashboard')