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
# SMALL HELPERS
# ----------------------------------------------------
def env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")

# ----------------------------------------------------
# BASIC DJANGO SETTINGS
# ----------------------------------------------------
SECRET_KEY = "django-insecure-*)ivux&@=t5v3uoh&#ozr1vvy3omnf%w1j5%w!_ktm*7359pl%"

# Default False, but can be turned ON from Azure with DJANGO_DEBUG=1
DEBUG = env_bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = [
    "doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net",
]

# ----------------------------------------------------
# OPENAI KEY
# ----------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY is missing! Check Azure App Settings or .env.")

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
# MIDDLEWARE
# ----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
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
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ----------------------------------------------------
# LOGGING – send errors to console (Azure Log Stream)
# ----------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# ----------------------------------------------------
# PRIMARY KEY FIELD
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
