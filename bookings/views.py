from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from doctors.models import Availability
from .models import Booking
from hospital_system.google_calendar import sync_event_to_google
import requests
from django.conf import settings

@login_required
@transaction.atomic
def book_slot(request, slot_id):
    slot = get_object_or_404(Availability, id=slot_id, is_booked=False)

    if request.user.role != "patient":
        return redirect("login")

    # lock row to avoid race condition
    slot = Availability.objects.select_for_update().get(id=slot_id)

    if slot.is_booked:
        return redirect("patient_dashboard")


    booking = Booking.objects.create(
        availability=slot,
        patient=request.user,
        doctor=slot.doctor,
    )

    slot.is_booked = True
    slot.save()

    # Google Calendar event for doctor
    event_doctor = CalendarEvent.objects.create(
        user=slot.doctor,
        title=f"Appointment with {request.user.username}",
        start_time=f"{slot.date}T{slot.start_time}",
        end_time=f"{slot.date}T{slot.end_time}",
        description=f"Patient: {request.user.username}"
    )
    sync_event_to_google(event_doctor)

    # Google Calendar event for patient
    event_patient = CalendarEvent.objects.create(
        user=request.user,
        title=f"Appointment with Dr. {slot.doctor.username}",
        start_time=f"{slot.date}T{slot.start_time}",
        end_time=f"{slot.date}T{slot.end_time}",
        description=f"Doctor: {slot.doctor.username}"
    )
    sync_event_to_google(event_patient)

    # Send booking confirmation email via serverless
    try:
        email_url = "http://localhost:4000/dev/send-email"
        requests.post(email_url, json={
            "action": "BOOKING_CONFIRMATION",
            "email": request.user.email,
            "name": request.user.username
        }, timeout=3)
    except Exception:
        pass

    return redirect("patient_dashboard")
