
from django.contrib import admin
from .models import Availability, DoctorCategory

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
	list_display = ("doctor", "category", "date", "start_time", "end_time", "is_booked")
	list_filter = ("category", "doctor", "date", "is_booked")

admin.site.register(DoctorCategory)
