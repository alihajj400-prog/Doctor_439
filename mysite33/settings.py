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
# LOAD .env (supports root/.env or mysite33/.env)
# ----------------------------------------------------
for env_path in (BASE_DIR / ".env", BASE_DIR / "mysite33" / ".env"):
    if env_path.exists():
        load_dotenv(env_path, override=True)

# ----------------------------------------------------
# OPENAI API KEY
# ----------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY is missing. Add it to your .env file.")

# ----------------------------------------------------
# BASIC DJANGO SETTINGS
# ----------------------------------------------------
SECRET_KEY = "django-insecure-*)ivux&@=t5v3uoh&#ozr1vvy3omnf%w1j5%w!_ktm*7359pl%"

# Azure production requires DEBUG = False
DEBUG = False

# REAL Azure hostname
AZURE_HOST = "doctor439webapp-cuaje0h0bzeggsax.canadacentral-01.azurewebsites.net"

ALLOWED_HOSTS = [
    AZURE_HOST,
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{AZURE_HOST}",
]

# ----------------------------------------------------
# INSTALLED APPS
# ----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # your app
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
# PASSWORD VALIDATION
# ----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# ----------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
# STATIC FILES (Azure requires STATIC_ROOT)
# ----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ----------------------------------------------------
# DEFAULT FIELD TYPE
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
