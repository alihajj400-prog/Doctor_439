from django import forms
from .models import Contact, AppointmentRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'specialty',
            'city',
            'hospital',
            'fees',
            'rating',
            'experience_years',
            'languages',
            'availability',
            'insurance_partners',
            'description',
            'photo_url',
            'contact_phone',
        ]


class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ['patient_name', 'patient_email', 'patient_phone', 'preferred_date', 'message']
