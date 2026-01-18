from django.contrib import admin
from django.urls import path, include

from accounts import views as account_views
from hospital_system import views
from doctors import views as doctor_views

urlpatterns = [
    # ROOT
    path("", views.home, name="home"),

    # AUTH
    path("login/", account_views.user_login, name="login"),
    path("signup/", account_views.user_signup, name="signup"),
    path("logout/", account_views.user_logout, name="logout"),

    # DOCTOR DASHBOARD & SLOT MANAGEMENT
    path("doctor/", include("doctors.urls")),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("patient/doctors/", views.patient_doctors, name="patient_doctors"),
    path("patient/doctor/<int:doctor_id>/", views.doctor_slots, name="doctor_slots"),
    path("patient/book/<int:slot_id>/", views.book_slot, name="book_slot"),

    # BOOKINGS APP
    path("bookings/", include("bookings.urls")),

    # ADMIN
    path("admin/", admin.site.urls),
]
