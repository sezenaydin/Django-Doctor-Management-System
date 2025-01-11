from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




app_name = 'office'

urlpatterns = [

     path('', views.home, name='home'),

    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('secretary-login/', views.secretary_login, name='secretary_login'),
    path('secretary-dashboard/', views.secretary_dashboard, name='secretary_dashboard'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/update/<int:pk>/', views.update_appointment, name='update_appointment'),
    path('appointments/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    
    path('add/', views.add_patient, name='add_patient'),
    path('update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('view/', views.view_patients, name='view_patients'),

    path('prescriptions/', views.list_prescriptions, name='list_prescriptions'),
    path('prescriptions/create/', views.create_prescription, name='create_prescription'),
    path('prescriptions/update/<int:pk>/', views.update_prescription, name='update_prescription'),
    path('prescriptions/delete/<int:pk>/', views.delete_prescription, name='delete_prescription'),


    path('patients/<int:patient_id>/medical-history/', views.view_patient_medical_history, name='patient_medical_history'),
    

    
    path('add-secretary/', views.add_secretary, name='add_secretary'),
    path('list-secretaries/', views.list_secretaries, name='list_secretaries'),
    path('update-secretary/<int:pk>/', views.update_secretary, name='update_secretary'),
    path('delete-secretary/<int:pk>/', views.delete_secretary, name='delete_secretary'),

    path('manage-working-days/', views.manage_working_days, name='manage_working_days'),
    path('clear-announcements/', views.clear_announcements, name='clear_announcements'),

]
