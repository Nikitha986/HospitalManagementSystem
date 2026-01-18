from django.db import models
from django.contrib.auth import get_user_model
from doctors.models import Availability

User = get_user_model()

class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Availability, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='booked')

    def __str__(self):
        return f"{self.patient.username} → {self.slot}"
