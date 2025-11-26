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


class IntakeSymptomForm(forms.Form):
    symptoms = forms.CharField(
        label="Describe the symptoms",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "e.g., persistent headaches, nausea, blurred vision"}),
    )
    duration = forms.CharField(
        label="How long has this been happening?",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g., 2 weeks"}),
    )


class IntakeDetailsForm(forms.Form):
    city = forms.CharField(
        label="City or area",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g., Beirut, Tripoli"}),
    )
    budget_direction = forms.ChoiceField(
        label="Budget preference",
        required=False,
        choices=[
            ("under", "Under / Less than"),
            ("over", "Over / More than"),
        ],
    )
    budget_amount = forms.IntegerField(
        label="Budget amount (USD)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "e.g., 600"}),
    )


class IntakeUrgencyForm(forms.Form):
    urgency = forms.ChoiceField(
        label="How urgent is this?",
        choices=[
            ("routine", "Routine (checkup or long-term issue)"),
            ("soon", "Soon (book within a week)"),
            ("urgent", "Urgent (within 48 hours)"),
        ],
        widget=forms.RadioSelect,
    )
    contact_name = forms.CharField(label="Your name", required=False)
    contact_email = forms.EmailField(label="Email (optional)", required=False)
    notes = forms.CharField(
        label="Extra notes",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
