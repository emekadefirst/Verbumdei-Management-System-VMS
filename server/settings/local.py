from .base import *
from dotenv import load_dotenv 

load_dotenv()

SECRET_KEY = os.environ.get('LOCAL_KEY')


ALLOWED_HOSTS = []

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "verbumdeiMS.db"
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("DATABASE_NAME"),
#         "USER": os.environ.get("DATABASE_USER"),
#         "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
#         "HOST": os.environ.get("DATABASE_HOST"),
#         "PORT": 5432,
#         "OPTIONS": {"sslmode": "require"},
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "koyebdb",
        "USER": "koyeb-adm",
        "PASSWORD": "ghCavbYw54IP",
        "HOST": "ep-bitter-math-a2fo0js2.eu-central-1.pg.koyeb.app",
        "OPTIONS": {"sslmode": "require"},
    }
}


CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "http://localhost:3000"]

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
