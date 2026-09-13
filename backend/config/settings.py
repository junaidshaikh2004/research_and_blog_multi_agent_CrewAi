import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Loaded explicitly (rather than relying on crewai_agent's own load_dotenv())
# so GROQ_API_KEY / MODEL are already in os.environ before views.py imports
# the crewai_agent package, which lives in a sibling directory dotenv can't find on its own.
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-secret-key")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = []

WSGI_APPLICATION = "config.wsgi.application"

# No database: this app is stateless, one-shot, nothing is persisted.
DATABASES = {}

USE_TZ = True

CORS_ALLOWED_ORIGINS = [os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")]
