from django.contrib.auth.models import AbstractUser 
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    google_credentials = models.JSONField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
pass

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_appointments')
    appointment_date = models.DateField(default=datetime.date.today)
    appointment_time = models.TimeField(default=timezone.now)
    service_type = models.CharField(max_length=100, choices=[
        ('General Checkup', 'General Checkup'),
        ('Consultation', 'Consultation'),
        ('Emergency', 'Emergency'),
        ('Follow-up', 'Follow-up'),
    ], default='General Checkup')
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ], default='Scheduled')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient_name} on {self.appointment_date} at {self.appointment_time}"





def default_end_date():
    return datetime.date.today() + datetime.timedelta(days=30)  


class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)

    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='add_prescription')
    patient_age = models.IntegerField(default=30)
    medication = models.TextField()
    dosage = models.CharField(max_length=100, default="N/A")
    frequency = models.CharField(max_length=100, default="Once a day")
    duration = models.CharField(max_length=100, default="30 days")
    instructions = models.CharField(max_length=255, default="No special instructions")
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=default_end_date)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.medication[:20]} - {self.dosage}"

class Patient(models.Model):
    name = models.CharField(max_length=100)  
    dob = models.DateField()  
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  
    email = models.EmailField(blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)  
    medications = models.TextField(blank=True, null=True) 
    complaints = models.TextField(blank=True, null=True)  
    allergies = models.TextField(blank=True, null=True)  
    medical_history = models.TextField(blank=True, null=True)  
    smoking = models.BooleanField(default=False)  
    alcohol = models.BooleanField(default=False) 
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)  
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name


class Secretary(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    hire_date = models.DateField()
    department = models.CharField(max_length=100, choices=[
        ('Administration', 'Administration'),
        ('Billing', 'Billing'),
        ('Patient Support', 'Patient Support'),
    ])
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



class WorkingDay(models.Model):
    DOCTOR_AVAILABILITY = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="working_days")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=DOCTOR_AVAILABILITY, default='Available')

    def __str__(self):
        return f"{self.doctor.username} - {self.date} ({self.status})"