import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


"""
admin
admin@verbumdei.com
adminv2.
"""

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

INSTALLED_APPS = [
    "unfold.contrib.import_export",
    "import_export",
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # packages
    "drf_yasg",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    # installed Apps
    "staff",
    "student",
    "parent",
    "program",
    "grade",
    "asessment",
    "inventory",
    "payment",
    "customuser",
    "term",
    "studentattendance",
    "library",
    "Dormitary",
    "transport",
    "result",
    "announcement",
    "voucher",
]

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "customuser.backend.CustomBackend",
]

AUTH_USER_MODEL = "customuser.CustomUser" 


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = ["static"]
STATIC_ROOT =  "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("media")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UNFOLD = {
    "SITE_TITLE": "Verbumdei MS",
    "SITE_HEADER": "Verbumdei Super Admin",
    "SITE_LOGO": lambda request: static("logo.jpeg"),
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("logo.jpeg"),
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": True,
    "SIDEBAR": {
        "show_search": True,
    },
    "COLORS": {
        "primary": {
            "50": "235 245 255",
            "100": "215 235 255",
            "200": "176 215 255",
            "300": "137 195 255",
            "400": "98 175 255",
            "500": "0 0 255",
            "600": "0 0 204",
            "700": "0 0 153",
            "800": "0 0 102",
            "900": "0 0 51",
            "950": "0 0 25",
        }
    },
    "DASHBOARD_CALLBACK": "server.utils.dashboard_callback",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("logo.jpeg"),
        },
    ],
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  
    ],
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Changed to True
EMAIL_HOST_USER = "emekadefirst@gmail.com"
EMAIL_HOST_PASSWORD = "pzrz urxv epvt gybj"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 20
