from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Contact
from .forms import ContactForm, AppointmentRequestForm

import csv
import os
import re
from difflib import get_close_matches
from urllib.parse import quote_plus


SPECIALTY_RULES = [
    {
        "name": "Cardiology",
        "keywords": ["heart", "cardio", "chest pain", "palpitation", "blood pressure", "angina"],
        "tip": "Cardiologists handle chest pain, rhythm problems, and circulation concerns.",
    },
    {
        "name": "Neurology",
        "keywords": ["headache", "migraine", "seizure", "numb", "stroke", "dizzy", "vertigo", "memory loss"],
        "tip": "Neurologists are best for migraines, dizziness, weakness, or seizure activity.",
    },
    {
        "name": "Dermatology",
        "keywords": ["skin", "rash", "acne", "itch", "eczema", "psoriasis", "mole", "hair loss"],
        "tip": "Dermatologists treat rashes, acne breakouts, hair issues, and suspicious moles.",
    },
    {
        "name": "Dentistry",
        "keywords": ["tooth", "teeth", "gum", "cavity", "jaw", "dental", "mouth", "toothache"],
        "tip": "Dentists manage toothaches, gum inflammation, jaw pain, and other dental issues.",
    },
    {
        "name": "Plastic Surgery",
        "keywords": ["cosmetic", "nose job", "rhinoplasty", "burn scar", "face lift", "aesthetic surgery"],
        "tip": "Plastic surgeons handle cosmetic adjustments, rhinoplasty, scar repair, and reconstruction.",
    },
    {
        "name": "Gastroenterology",
        "keywords": [
            "stomach",
            "abdomen",
            "digestion",
            "ulcer",
            "ibs",
            "acid reflux",
            "constipation",
            "bloating",
            "cramp",
        ],
        "tip": "Gastroenterologists cover abdominal pain, reflux, constipation, bloating, and ulcers.",
    },
    {
        "name": "Hepatology",
        "keywords": ["liver", "hepatitis", "cirrhosis", "jaundice", "fatty liver"],
        "tip": "Hepatologists take care of liver inflammation, hepatitis, and jaundice.",
    },
    {
        "name": "Orthopedics",
        "keywords": [
            "joint",
            "knee",
            "back pain",
            "bone",
            "fracture",
            "spine",
            "shoulder",
            "elbow",
            "hip",
            "sprain",
        ],
        "tip": "Orthopedic doctors focus on bones, joints, shoulder problems, and chronic back pain.",
    },
    {
        "name": "Neurosurgery",
        "keywords": ["brain tumor", "spinal cord", "back surgery", "head injury", "neuro surgery"],
        "tip": "Neurosurgeons evaluate complex brain, spine, and nerve compression cases.",
    },
    {
        "name": "Cardiothoracic Surgery",
        "keywords": ["bypass", "heart surgery", "open heart", "valve replacement", "thoracic"],
        "tip": "Cardiothoracic surgeons handle heart valve repairs, bypass operations, and chest procedures.",
    },
    {
        "name": "Sports Medicine",
        "keywords": ["sports injury", "pulled muscle", "tendon", "runner", "athletic"],
        "tip": "Sports medicine specialists treat exercise injuries, tendon pain, and rehab plans.",
    },
    {
        "name": "Pulmonology",
        "keywords": ["cough", "asthma", "shortness of breath", "lungs", "wheezing", "bronchitis"],
        "tip": "Pulmonologists treat asthma, chronic cough, bronchitis, and breathing troubles.",
    },
    {
        "name": "Endocrinology",
        "keywords": ["diabetes", "thyroid", "hormone", "pcos", "weight gain", "metabolism"],
        "tip": "Endocrinologists cover diabetes management, thyroid imbalance, and hormone disorders.",
    },
    {
        "name": "Psychiatry",
        "keywords": ["anxiety", "depression", "panic", "mental", "stress", "insomnia", "mood"],
        "tip": "Psychiatrists support depression, anxiety, sleep issues, and stress disorders.",
    },
    {
        "name": "ENT",
        "keywords": ["ear", "throat", "sinus", "tonsil", "hearing", "nose bleed", "congestion"],
        "tip": "ENT specialists treat ear infections, sinus problems, and throat pain.",
    },
    {
        "name": "Facial Plastic Surgery",
        "keywords": ["nose surgery", "septoplasty", "broken nose", "deviated septum"],
        "tip": "Facial plastic surgeons focus on nose/septum repairs and complex facial injuries.",
    },
    {
        "name": "Ophthalmology",
        "keywords": ["eye", "vision", "blurred", "red eye", "cataract", "dry eye"],
        "tip": "Ophthalmologists manage eye pain, blurred sight, infections, and cataracts.",
    },
    {
        "name": "Urology",
        "keywords": ["urine", "kidney stone", "bladder", "prostate", "peeing", "urinary"],
        "tip": "Urologists handle kidney stones, urinary tract infections, and prostate issues.",
    },
    {
        "name": "Gynecology",
        "keywords": ["pregnancy", "period", "menstrual", "fertility", "ovary", "pelvic"],
        "tip": "Gynecologists help with menstrual cycles, fertility, pregnancies, and pelvic pain.",
    },
    {
        "name": "Pediatrics",
        "keywords": ["child", "kid", "baby", "infant", "toddler", "pediatric"],
        "tip": "Pediatricians care for infants, toddlers, and children with growth or illness concerns.",
    },
    {
        "name": "Allergy & Immunology",
        "keywords": ["allergy", "sneeze", "hay fever", "immune", "hives", "allergic"],
        "tip": "Allergists diagnose seasonal allergies, hives, and immune over-reactions.",
    },
    {
        "name": "Emergency Medicine",
        "keywords": ["trauma", "accident", "bleeding", "emergency", "urgent", "collapse"],
        "tip": "Emergency medicine physicians stabilize fractures, trauma wounds, sudden collapses, or accidents.",
    },
    {
        "name": "Infectious Disease",
        "keywords": ["infection", "covid", "feverish", "antibiotic", "virus", "bacteria"],
        "tip": "Infectious disease doctors manage hard-to-treat infections, fevers, and travel bugs.",
    },
    {
        "name": "Nephrology",
        "keywords": ["kidney", "renal", "protein in urine", "dialysis", "swollen feet"],
        "tip": "Nephrologists focus on kidney disease, swelling, and electrolyte problems.",
    },
    {
        "name": "Rheumatology",
        "keywords": ["arthritis", "autoimmune", "joint swelling", "lupus", "gout"],
        "tip": "Rheumatologists treat arthritis, autoimmune inflammation, gout, and joint swelling.",
    },
    {
        "name": "Oncology",
        "keywords": ["cancer", "tumor", "chemotherapy", "mass", "lesion"],
        "tip": "Oncologists coordinate cancer evaluations, biopsies, and treatment plans.",
    },
    {
        "name": "Hematology",
        "keywords": ["blood", "anemia", "platelet", "clotting", "hemoglobin"],
        "tip": "Hematologists evaluate anemia, clotting disorders, and abnormal blood tests.",
    },
    {
        "name": "General Surgery",
        "keywords": ["surgery", "surgeon", "hernia", "appendix", "gallbladder", "laparoscopic"],
        "tip": "General surgeons handle abdominal operations such as gallbladder removal, hernia repairs, and biopsies.",
    },
    {
        "name": "General Medicine",
        "keywords": ["fever", "flu", "cold", "tired", "fatigue", "checkup", "weakness"],
        "tip": "A general practitioner can review fever, fatigue, or overall health changes.",
    },
]

SPECIALTY_NAME_MAP = {rule["name"].lower(): rule for rule in SPECIALTY_RULES}

SPECIALTY_ALIASES = {
    "appendicitis": "General Surgery",
    "gallstones": "General Surgery",
    "hernia": "General Surgery",
    "burn": "Plastic Surgery",
    "nosebleed": "ENT",
    "eczema": "Dermatology",
    "psoriasis": "Dermatology",
    "melanoma": "Dermatology",
    "migraine": "Neurology",
    "epilepsy": "Neurology",
    "stroke": "Neurology",
    "diabetes": "Endocrinology",
    "thyroiditis": "Endocrinology",
    "pcos": "Endocrinology",
    "covid": "Infectious Disease",
    "influenza": "Infectious Disease",
    "bronchitis": "Pulmonology",
    "asthma": "Pulmonology",
    "pneumonia": "Pulmonology",
    "kidney stone": "Urology",
    "prostatitis": "Urology",
    "uti": "Urology",
    "fertility": "Gynecology",
    "pregnancy": "Gynecology",
    "infertility": "Gynecology",
    "arthritis": "Rheumatology",
    "lupus": "Rheumatology",
    "gout": "Rheumatology",
    "anemia": "Hematology",
    "leukemia": "Oncology",
    "tumor": "Oncology",
    "depression": "Psychiatry",
    "anxiety": "Psychiatry",
    "adhd": "Psychiatry",
    "sciatica": "Orthopedics",
    "fracture": "Orthopedics",
    "back injury": "Orthopedics",
    "ulcer": "Gastroenterology",
    "ibs": "Gastroenterology",
    "cirrhosis": "Hepatology",
    "jaundice": "Hepatology",
    "allergy": "Allergy & Immunology",
    "hives": "Allergy & Immunology",
    "sepsis": "Emergency Medicine",
}

SMART_TIPS = {
    "Cardiology": {
        "tip": "Monitor chest discomfort, shortness of breath, or unusual fatigue while waiting for a consult.",
        "checklist": [
            "Record when symptoms appear and what triggers them (exercise, meals, stress).",
            "Bring blood pressure logs, ECG results, or medication lists.",
            "Avoid heavy caffeine 12 hours before the appointment unless advised otherwise.",
        ],
    },
    "Dermatology": {
        "tip": "Capture photos of skin changes in good light so the doctor can track progress.",
        "checklist": [
            "List skincare products and medications used in the last two weeks.",
            "Avoid new peels/creams for 48 hours before the visit.",
            "Note any allergies to antibiotics or topical treatments.",
        ],
    },
    "Orthopedics": {
        "tip": "Rest the affected joint but maintain gentle range-of-motion exercises if possible.",
        "checklist": [
            "Bring prior imaging (X-ray, MRI) or request transfers from previous clinics.",
            "Note pain levels and movements that worsen the issue.",
            "Wear clothing that allows the joint to be examined easily.",
        ],
    },
    "Pediatrics": {
        "tip": "Track your child’s temperature, hydration, and behavior changes until the appointment.",
        "checklist": [
            "Carry the vaccination booklet and recent lab results.",
            "List medications or home remedies already tried.",
            "Prepare questions about sleep, school, or feeding routines.",
        ],
    },
    "General Medicine": {
        "tip": "A GP can triage most concerns quickly and direct you to specialists if needed.",
        "checklist": [
            "Summarize key symptoms with start dates.",
            "List medications or supplements you take regularly.",
            "Bring recent blood tests or blood pressure readings if available.",
        ],
    },
}

DEFAULT_SPECIALTIES = [rule["name"] for rule in SPECIALTY_RULES[:8]]


def detect_specialty(user_msg: str):
    text = user_msg.lower()

    # 1) direct specialty name
    for rule in SPECIALTY_RULES:
        if rule["name"].lower() in text:
            return rule

    # 2) keyword rules
    for rule in SPECIALTY_RULES:
        if any(keyword in text for keyword in rule["keywords"]):
            return rule

    # 3) explicit aliases
    for term, specialty_name in SPECIALTY_ALIASES.items():
        if term in text:
            return SPECIALTY_NAME_MAP.get(specialty_name.lower())

    # 4) fuzzy matching on specialty names
    words = re.findall(r"[a-zA-Z]+", text)
    names = list(SPECIALTY_NAME_MAP.keys())
    for token in words:
        if len(token) < 4:
            continue
        close = get_close_matches(token, names, n=1, cutoff=0.78)
        if close:
            return SPECIALTY_NAME_MAP[close[0]]

    # 5) fuzzy on alias keys
    alias_keys = list(SPECIALTY_ALIASES.keys())
    for token in words:
        if len(token) < 4:
            continue
        close = get_close_matches(token, alias_keys, n=1, cutoff=0.82)
        if close:
            specialty_name = SPECIALTY_ALIASES[close[0]]
            return SPECIALTY_NAME_MAP.get(specialty_name.lower())

    # 6) default
    return SPECIALTY_NAME_MAP.get("general medicine")


def detect_city(user_msg: str):
    text = user_msg.lower()
    cities = Contact.objects.values_list("city", flat=True).distinct()
    for city in cities:
        city_lower = (city or "").lower()
        if city_lower and city_lower in text:
            return city
    return None


def detect_budget(user_msg: str):
    text = user_msg.lower()
    match = re.search(r"(?:under|below|less than)\s*\$?\s*(\d{2,5})", text)
    if not match:
        match = re.search(r"(?:budget|fees?)\s*(?:around|about|near)?\s*\$?\s*(\d{2,5})", text)
    if match:
        try:
            amount = int(match.group(1))
            return amount, f"Budget ≤ ${amount}"
        except ValueError:
            return None
    return None


# -------------------------------------------------------
# CHATBOT (POST from JS) – CSRF exempt
# -------------------------------------------------------
@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    user_msg = request.POST.get("message", "").strip()
    if not user_msg:
        return JsonResponse({"reply": "Please type a message."})

    try:
        rule = detect_specialty(user_msg)
        city = detect_city(user_msg)
        budget_info = detect_budget(user_msg)

        if rule:
            specialty = rule["name"]
            answer = rule["tip"]

            doctors_qs = Contact.objects.filter(specialty__icontains=specialty)

            notes = []

            if budget_info:
                max_fee, msg = budget_info
                doctors_qs = doctors_qs.filter(fees__lte=max_fee)
                notes.append(msg)

            if city:
                city_matches = doctors_qs.filter(city__icontains=city)
                if city_matches.exists():
                    doctors_qs = city_matches
                    notes.append(f"Showing doctors near {city}.")
                else:
                    notes.append(
                        f"No saved {specialty} doctors in {city}, so here are the top-rated options."
                    )
            else:
                notes.append("Showing top matches from your directory.")

            doctors = doctors_qs.order_by("-rating")[:5]

            if doctors:
                doc_lines = [
                    f"• **{d.name}** – {d.city}, {d.hospital}, Rating: {d.rating} ⭐"
                    for d in doctors
                ]
                doctor_text = "\n".join(doc_lines)
            else:
                doctor_text = "No doctors saved yet for this specialty."

            note_text = "\n".join(f"• {n}" for n in notes if n)
            smart_tip = SMART_TIPS.get(specialty, SMART_TIPS["General Medicine"])
            checklist = "\n".join(f"- {item}" for item in smart_tip.get("checklist", []))

            reply = (
                f"{answer}\n\n"
                f"{note_text}\n\n"
                f"**Recommended specialty:** {specialty}\n\n"
                f"**Top doctors in our directory:**\n{doctor_text}\n\n"
                f"**AI health tip:** {smart_tip.get('tip')}\n"
                f"**Preparation checklist:**\n{checklist}"
            )
        else:
            reply = (
                "Hi there! Tell me about a symptom, a body part, or the type of doctor you want "
                "(for example 'rash on arm', 'dentist in Beirut', 'budget under 600') and I’ll "
                "point you to the best fits."
            )

        return JsonResponse({"reply": reply})
    except Exception as e:
        print("Chatbot error:", e)
        return JsonResponse({"reply": "Error processing request."})


# -------------------------------------------------------
# FAVORITES UTIL
# -------------------------------------------------------
def get_favorite_ids(request):
    return set(request.session.get("favorite_doctors", []))


def save_favorite_ids(request, ids):
    request.session["favorite_doctors"] = list(ids)
    request.session.modified = True


# -------------------------------------------------------
# HOME (CREATE + LIST) – CSRF exempt to avoid 403 on Azure
# -------------------------------------------------------
@csrf_exempt
def home(request):
    query = request.GET.get("search", "").strip()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ContactForm()

    contacts = Contact.objects.order_by("-id")
    if query:
        contacts = contacts.filter(name__icontains=query)

    favorites = get_favorite_ids(request)

    return render(
        request,
        "myapp33/createcontact.html",
        {
            "form": form,
            "contacts": contacts,
            "favorites": favorites,
            "search": query,
        },
    )


# -------------------------------------------------------
# EDIT CONTACT – CSRF exempt
# -------------------------------------------------------
@csrf_exempt
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ContactForm(instance=contact)

    return render(request, "myapp33/editcontact.html", {"form": form, "contact": contact})


# -------------------------------------------------------
# DELETE CONTACT – POST only + CSRF exempt
# -------------------------------------------------------
@csrf_exempt
@require_POST
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect("home")


# -------------------------------------------------------
# LOAD DOCTORS FROM CSV (ONE-TIME IMPORT)
# -------------------------------------------------------
def load_doctors(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "doctors.csv")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        Contact.objects.all().delete()

        for row in reader:
            Contact.objects.create(
                name=row["name"],
                specialty=row.get("specialty", ""),
                city=row.get("city", ""),
                hospital=row.get("hospital", ""),
                fees=int(row.get("fees", 0)),
                rating=float(row.get("rating", 0)),
            )

    return HttpResponse(f"Loaded {Contact.objects.count()} doctors.")


# -------------------------------------------------------
# RECOMMENDATION ENGINE (FILTER + SORT)
# -------------------------------------------------------
def recommend_doctors(request):
    city = request.GET.get("city", "")
    specialty = request.GET.get("specialty", "")
    max_fees = request.GET.get("max_fees", "")
    min_rating = request.GET.get("min_rating", "")
    sort = request.GET.get("sort", "rating_desc")
    query = request.GET.get("search", "").strip()

    qs = Contact.objects.all()

    if query:
        qs = qs.filter(name__icontains=query)

    if city:
        qs = qs.filter(city__icontains=city)

    if specialty:
        qs = qs.filter(specialty__icontains=specialty)

    if max_fees:
        try:
            qs = qs.filter(fees__lte=int(max_fees))
        except ValueError:
            pass

    if min_rating:
        try:
            qs = qs.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    if sort == "rating_desc":
        qs = qs.order_by("-rating")
    elif sort == "rating_asc":
        qs = qs.order_by("rating")
    elif sort == "fees_asc":
        qs = qs.order_by("fees")
    elif sort == "fees_desc":
        qs = qs.order_by("-fees")
    else:
        qs = qs.order_by("-rating")

    city_choices = (
        Contact.objects.values_list("city", flat=True).distinct().order_by("city")
    )
    specialty_choices = (
        Contact.objects.values_list("specialty", flat=True)
        .distinct()
        .order_by("specialty")
    )

    favorites = get_favorite_ids(request)

    return render(
        request,
        "myapp33/recommend.html",
        {
            "results": qs,
            "city_choices": city_choices,
            "specialty_choices": specialty_choices,
            "city": city,
            "specialty": specialty,
            "max_fees": max_fees,
            "min_rating": min_rating,
            "sort": sort,
            "favorites": favorites,
            "search": query,
        },
    )


# -------------------------------------------------------
# DOCTOR PROFILE PAGE
# -------------------------------------------------------
def doctor_detail(request, pk):
    doctor = get_object_or_404(Contact, pk=pk)
    appointment_form = AppointmentRequestForm()

    if request.method == "POST":
        appointment_form = AppointmentRequestForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.doctor = doctor
            appointment.save()
            messages.success(
                request,
                "Thanks! Your request was sent to the clinic team. They will contact you soon.",
            )
            return redirect("doctor_detail", pk=doctor.pk)

    reviews = [
        {
            "name": "Maya S.",
            "rating": 5,
            "date": "May 2024",
            "text": "Very attentive and thorough. Explained every step of the treatment plan.",
        },
        {
            "name": "Nabil H.",
            "rating": 4,
            "date": "Jan 2024",
            "text": "Clinic was clean and organized. Short waiting time and great follow-up.",
        },
        {
            "name": "Selene A.",
            "rating": 5,
            "date": "Aug 2023",
            "text": "Helped me recover quickly. Highly recommend for anyone in Lebanon.",
        },
    ]

    languages = [
        item.strip()
        for item in (doctor.languages or "Arabic, English").split(",")
        if item.strip()
    ]
    insurance_partners = [
        item.strip()
        for item in (doctor.insurance_partners or "Medicare, Allianz, Bankers").split(
            ","
        )
        if item.strip()
    ]

    similar_doctors = (
        Contact.objects.filter(specialty__iexact=doctor.specialty)
        .exclude(pk=doctor.pk)
        .order_by("-rating")[:4]
    )

    favorites = get_favorite_ids(request)
    is_favorite = doctor.pk in favorites
    whatsapp_message = quote_plus(
        f"Hello, I'm interested in booking with {doctor.name} ({doctor.specialty}) in {doctor.city}. "
        "Could you help me schedule an appointment?"
    )
    whatsapp_url = f"https://wa.me/?text={whatsapp_message}"

    return render(
        request,
        "myapp33/doctor_detail.html",
        {
            "doctor": doctor,
            "reviews": reviews,
            "similar_doctors": similar_doctors,
            "appointment_form": appointment_form,
            "languages": languages,
            "insurance_partners": insurance_partners,
            "is_favorite": is_favorite,
            "whatsapp_url": whatsapp_url,
        },
    )


# -------------------------------------------------------
# TOGGLE FAVORITE – POST only + CSRF exempt
# -------------------------------------------------------
@csrf_exempt
@require_POST
def toggle_favorite(request, pk):
    doctor = get_object_or_404(Contact, pk=pk)
    favorites = get_favorite_ids(request)

    if doctor.pk in favorites:
        favorites.remove(doctor.pk)
        messages.info(request, f"Removed {doctor.name} from your shortlist.")
    else:
        favorites.add(doctor.pk)
        messages.success(request, f"Added {doctor.name} to your shortlist.")

    save_favorite_ids(request, favorites)
    redirect_to = (
        request.POST.get("next")
        or request.META.get("HTTP_REFERER")
        or "home"
    )
    return HttpResponseRedirect(redirect_to)


# -------------------------------------------------------
# FAVORITES LIST PAGE
# -------------------------------------------------------
def favorite_list(request):
    favorites = get_favorite_ids(request)
    doctors = Contact.objects.filter(pk__in=favorites)
    selected = request.GET.getlist("compare")[:3]
    compare_doctors = Contact.objects.filter(pk__in=selected)

    return render(
        request,
        "myapp33/favorites.html",
        {
            "doctors": doctors,
            "favorites": favorites,
            "compare_doctors": compare_doctors,
            "selected_compare": selected,
        },
    )


# -------------------------------------------------------
# HEALTH HUB STATIC CONTENT
# -------------------------------------------------------
def health_hub(request):
    articles = [
        {
            "title": "Cardiology vs. General Medicine: where to start?",
            "summary": "Learn when chest discomfort needs a cardiologist and what questions to bring to the first visit.",
            "tag": "Heart Health",
        },
        {
            "title": "Preparing for your first dermatology visit",
            "summary": "Dermatologists need a full picture of your skin routine. Download our checklist and photo tips.",
            "tag": "Skin",
        },
        {
            "title": "Children’s fever guide",
            "summary": "A pediatrician-approved flow of when to monitor at home, when to call, and what to pack for the clinic.",
            "tag": "Pediatrics",
        },
        {
            "title": "Orthopedic injury recovery",
            "summary": "From sprains to fractures, understand the phases of healing and partnering with physiotherapy.",
            "tag": "Mobility",
        },
    ]
    return render(request, "myapp33/health_hub.html", {"articles": articles})
