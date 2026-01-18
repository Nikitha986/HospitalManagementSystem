# 🏥 Mini Hospital Management System (HMS)

A role-based **Hospital Management System** built using **Django** that enables doctors to manage availability and patients to book appointments, with **Google Calendar integration** and a **serverless email notification service**.

---

## 🚀 Project Overview

This project demonstrates:
- Role-based authentication (Doctor / Patient)
- Appointment booking with slot locking
- Google Calendar API integration
- Serverless email notifications using AWS Lambda (local demo)

---

## 👥 User Roles

### 👨‍⚕️ Doctor
- Sign up & login
- Doctor dashboard
- Create and manage availability slots
- View only their own bookings
- Google Calendar event creation on booking

### 🧑‍💼 Patient
- Sign up & login
- Patient dashboard
- View doctors and available slots
- Book appointments
- Prevents double booking
- Google Calendar event creation on booking

---

## 🛠 Tech Stack

### Backend
- Django 4.2
- PostgreSQL
- Django ORM
- Session-based authentication

### Integrations
- Google Calendar API (OAuth2)
- Serverless email service (AWS Lambda – local using serverless-offline)


---
## 🛡 Admin (System Administrator)

The system also includes an **Admin role** powered by Django’s built-in admin panel.

### Admin Capabilities
- Secure admin login via Django Admin
- View and manage:
  - Doctors
  - Patients
  - Availability slots
  - Bookings
  - Google OAuth tokens
- Perform CRUD operations for troubleshooting and monitoring
- Acts as a system-level supervisor (not involved in booking flow)

### Admin Access
- Admin panel URL: http://127.0.0.1:8000/admin/


## 🔐 Authentication & Authorization

- Secure password hashing (Django default)
- Role-based access control
- Doctors and patients have isolated dashboards and permissions

---

## 📅 Booking Workflow

1. Patient selects:
   - Doctor
   - Date
   - Available time slot
2. System verifies slot availability
3. Booking is created atomically
4. Slot is locked (cannot be double-booked)
5. Google Calendar event created for:
   - Doctor
   - Patient
6. Confirmation email sent via serverless email service

---

## 📆 Google Calendar Integration

- OAuth2 authentication
- One Google account per user
- Event includes:
  - Title
  - Start & end time
  - Doctor & patient details

---

## 📧 Serverless Email Service

### Supported Email Types
- SIGNUP_WELCOME
- BOOKING_CONFIRMATION

### Implementation
- AWS Lambda (Python)
- Serverless Framework
- serverless-offline for local testing
- SMTP-based email delivery

---

## 🧪 Local Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Nikitha986/HospitalManagementSystem.git
cd HospitalManagementSystem



