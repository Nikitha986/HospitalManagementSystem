from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Root URL handler.
    Redirects users based on auth & role.
    """
    if request.user.is_authenticated:
        if request.user.role == "doctor":
            return redirect("doctor_dashboard")
        return redirect("patient_dashboard")
    return redirect("login")






from doctors.models import Availability, DoctorCategory
from bookings.models import Booking
from accounts.models import User
from django.utils import timezone
from django.core.mail import send_mail
from hospital_system.google_calendar import sync_event_to_google
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def patient_dashboard(request):
    # Link to doctor list
    return render(request, "patient_dashboard.html")


@login_required
def doctor_list(request):
    # Not used, replaced by patient_doctors
    doctors = User.objects.filter(role='DOCTOR')
    return render(request, "doctor_list.html", {'doctors': doctors})

@login_required
def patient_doctors(request):
    categories = DoctorCategory.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        doctor_ids = Availability.objects.filter(category_id=selected_category).values_list('doctor', flat=True).distinct()
        doctors = User.objects.filter(role='DOCTOR', id__in=doctor_ids)
    else:
        doctors = User.objects.filter(role='DOCTOR')
    return render(request, "patient_doctors.html", {
        'doctors': doctors,
        'categories': categories,
        'selected_category': selected_category or ""
    })

@login_required
def doctor_slots(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, role='DOCTOR')
    slots = Availability.objects.filter(doctor=doctor).order_by('date', 'start_time')
    return render(request, "doctor_slots.html", {'doctor': doctor, 'slots': slots})

@login_required
def book_slot(request, slot_id):
    print("[DEBUG] book_slot view called")
    slot = get_object_or_404(Availability, id=slot_id, is_booked=False)
    if request.user.role != 'PATIENT':
        messages.error(request, 'Only patients can book slots.')
        return redirect('patient_doctors')
    # Book the slot
    booking = Booking.objects.create(patient=request.user, slot=slot)
    print("[DEBUG] About to call sync_event_to_google")
    sync_event_to_google(slot)
    print("[DEBUG] Finished call to sync_event_to_google")
    slot.is_booked = True
    slot.save()

    # Email details
    doctor = slot.doctor
    patient = request.user
    subject = f"Appointment Booked: {slot.date} {slot.start_time}-{slot.end_time}"
    slot_info = f"Date: {slot.date}\nTime: {slot.start_time} - {slot.end_time}\nDoctor: Dr. {doctor.username}\nPatient: {patient.username}"
    print(f"[DEBUG] Sending email to patient: {patient.email}")
    send_mail(
        subject,
        f"Your appointment is confirmed.\n\n{slot_info}",
        None,
        [patient.email],
        fail_silently=True,
    )
    print(f"[DEBUG] Sending email to doctor: {doctor.email}")
    send_mail(
        subject,
        f"A patient has booked your slot.\n\n{slot_info}",
        None,
        [doctor.email],
        fail_silently=True,
    )
    print("[DEBUG] Emails sent.")

    messages.success(request, 'Slot booked successfully! Email notifications sent.')
    return redirect('patient_doctors')
