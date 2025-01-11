from django import forms
from .models import Appointment
from .models import Prescription
from .models import Patient,User
from .models import Secretary,WorkingDay


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'appointment_date', 'appointment_time', 'service_type', 'status', 'notes','doctor']


        doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_doctor=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )


    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    def clean_date(self):
        date = self.cleaned_data['date']
        doctor = self.cleaned_data.get('doctor')

        if doctor:
            
            if not WorkingDay.objects.filter(date=date, doctor=doctor, status='Available').exists():
                raise forms.ValidationError("The doctor is unavailable on the selected date. Please choose another date.")
        return date


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient_name', 'patient_age','doctor', 'medication', 'dosage', 'frequency', 'duration', 'instructions', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),


        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'gender', 'phone', 'email', 'address', 'medications', 'complaints', 
                  'allergies', 'medical_history', 'smoking', 'alcohol', 'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),  
        }


class SecretaryForm(forms.ModelForm):
    class Meta:
        model = Secretary
        fields = [
            'name', 
            'email', 
            'phone', 
            'address', 
            'hire_date', 
            'department', 
            'emergency_contact', 
            'notes'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class WorkingDayForm(forms.ModelForm):
    class Meta:
        model = WorkingDay
        fields = ['date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }