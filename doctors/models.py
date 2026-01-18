
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class DoctorCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(DoctorCategory, on_delete=models.SET_NULL, null=True, blank=True, help_text="Category the doctor belongs to")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)


    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        cat = f"[{self.category}] " if self.category else ""
        return f"{cat}{self.doctor.username} | {self.date} {self.start_time}-{self.end_time}"
