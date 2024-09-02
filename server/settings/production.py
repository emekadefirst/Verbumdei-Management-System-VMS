from .base import *
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("PRODUCTION_KEY")

ALLOWED_HOSTS = ["*"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Serve static files with WhiteNoise
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Serve media files with WhiteNoise
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "server/media")

# Custom storage classes (if you have them)
DEFAULT_FILE_STORAGE = (
    "django.core.files.storage.FileSystemStorage"  # Default Django storage
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "OPTIONS": {"sslmode": "require"},
    }
}

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "http://localhost:3000"]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
