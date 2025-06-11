# Django Doctor's Office Management System

## Overview

This project is a web-based appointment management system built with Django. It provides separate dashboards and features for doctors and secretaries, enabling streamlined management of appointments, patient records, prescriptions, and integration with Google Calendar.

## Features

### General
- **User Authentication**: Separate logins for doctors and secretaries.

### Doctor Features
- **Appointment Management**:
  - View scheduled appointments.
  - Block unavailable times 
- **Patient Management**:
  - View patient records and medical history.
- **Prescription Management**:
  - Create, update, and delete prescriptions.
- **Secretary Management**:
  - Add new secretaries and manage existing ones.
- **Google Calendar Integration**:
  - Sync availabilities and appointments with Google Calendar.
  
- **Doctor Dashboard**:
  - **Cards**:
    - Prescriptions: Manage prescriptions for patients.
    - Manage Schedule: Block unavailable times and adjust availability.
    - Add Secretary: Add new secretaries to the system.
    - Manage Secretaries: View and manage the list of secretaries.
  - **Lists**:
    - Scheduled appointments.
    - Patient records.

### Secretary Features
- **Appointment Management**:
  - Create, update, delete appointments.
  - Ensure appointments are only scheduled during available times.
- **Patient Management**:
  - Add, update, delete patient records.
  - Add patient medical history.

- **Secretary Dashboard**:
  - **Cards**:
    - Appointment Management: Manage appointment schedules.
    - Patient Records: Handle patient data.
    - Secretary Register: Register new secretaries into the system.
  - **Announcements Section**:
    - View the hours that the doctor has blocked, prescriptions that have been written, and the newly added secretary record.

## Usage
- **Access the application: Navigate to http://127.0.0.1:8000.**


