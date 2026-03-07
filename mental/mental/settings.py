"""
Django settings for mental project.
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = os.path.join(BASE_DIR, ".env")

print("Loading ENV from:", ENV_PATH)

load_dotenv(ENV_PATH)




# SECURITY
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-=s&5w=no)#ddfj&wk#@79ofuoh51h&*)pss30fy((e^a)!92*%",
)

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

allowed_hosts = os.getenv("ALLOWED_HOSTS", "")
if allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Applications
INSTALLED_APPS = [
    "home",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "mental.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "mental.wsgi.application"


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
