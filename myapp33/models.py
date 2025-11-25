from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    hospital = models.CharField(max_length=100, blank=True)
    fees = models.IntegerField()
    rating = models.FloatField()
    experience_years = models.PositiveIntegerField(default=5)
    languages = models.CharField(max_length=150, blank=True)
    availability = models.CharField(max_length=120, blank=True)
    insurance_partners = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} - {self.specialty} ({self.city})"


class AppointmentRequest(models.Model):
    doctor = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="appointments")
    patient_name = models.CharField(max_length=120)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=30, blank=True)
    preferred_date = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} -> {self.doctor.name}"
