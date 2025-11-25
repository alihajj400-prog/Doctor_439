"""
Django settings for mysite33 project.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# ----------------------------------------------------
# PATHS
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# LOAD .env FILE(S)
# ----------------------------------------------------
for env_file in (BASE_DIR / ".env", BASE_DIR / "mysite33" / ".env"):
    if env_file.exists():
        load_dotenv(env_file, override=True)

# ----------------------------------------------------
# OPENAI KEY (from .env)
# ----------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY is missing! Check your .env file.")

# ----------------------------------------------------
# BASIC DJANGO SETTINGS
# ----------------------------------------------------
SECRET_KEY = "django-insecure-*)ivux&@=t5v3uoh&#ozr1vvy3omnf%w1j5%w!_ktm*7359pl%"
DEBUG = True  # set to False later if you want

ALLOWED_HOSTS = [
    "doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net",
    "http://doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net",
]

# Optional but good on Azure behind HTTPS proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ----------------------------------------------------
# APPS
# ----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp33.apps.Myapp33Config",
]

# ----------------------------------------------------
# MIDDLEWARE  (CSRF DISABLED FOR THIS PROJECT)
# ----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # CSRF disabled so POSTs from Azure work without errors.
    # DO NOT DO THIS ON A REAL PRODUCTION SITE.
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------------------------------
# URLS / TEMPLATES
# ----------------------------------------------------
ROOT_URLCONF = "mysite33.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite33.wsgi.application"

# ----------------------------------------------------
# DATABASE
# ----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ----------------------------------------------------
# PASSWORDS
# ----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# ----------------------------------------------------
# LANGUAGE & TIMEZONE
# ----------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
# STATIC FILES
# ----------------------------------------------------
# Where static files are served from in URLs
STATIC_URL = "/static/"

# Where collectstatic puts files (Azure will serve these)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Where your source static files live (CSS, JS, images)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ----------------------------------------------------
# PRIMARY KEY FIELD
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
