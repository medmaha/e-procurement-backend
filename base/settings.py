import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
# DEBUG = bool(int(os.getenv("DEBUG") or 0))
DEBUG = True

ALLOWED_HOSTS = [
    "129.151.181.32",
    "127.0.0.1",
    "localhost",
    "e-procurement-backend-bp56.onrender.com",
]

CORS_ALLOWED_ORIGINS = [os.environ.get("CLIENT_HOST")]

AUTH_USER_MODEL = "accounts.Account"

LOGIN_URL = "/account/login/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    # "django_cron",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    # My projects
    "apps.core",
    "apps.accounts",
    "apps.vendors",
    "apps.dashboard",
    "apps.organization",
    "apps.gppa",
    "apps.procurement",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "apps.core.middlewares.permissions.PermissionGroupMiddleware",
]

ROOT_URLCONF = "base.urls"

TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "public/templates"],
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "apps.core.processors.meta_processor.app_company",
                # "apps.core.processors.page_processor.page_headings",
            ],
        },
    },
]

WSGI_APPLICATION = "base.wsgi.application"

X_FRAME_OPTIONS = "SAMEORIGIN"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db" / "db.sqlite3",
    }
}
# DATABASES = {
#     "default": {
#         "NAME": os.getenv("DATABASE_NAME"),
#         "USER": os.getenv("DATABASE_USER"),
#         "HOST": os.getenv("DATABASE_HOST"),
#         "PORT": os.getenv("DATABASE_PORT"),
#         "PASSWORD": os.getenv("DATABASE_PASSWORD"),
#         "ENGINE": os.getenv("DATABASE_ENGINE"),
#     }
# }


EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 0))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True

MEDIA_URL = "media/"
STATIC_URL = "static/"
STATICFILES_DIRS = (BASE_DIR / "public/",)

MEDIA_ROOT = os.path.join(BASE_DIR, "public/dist/media/")
STATIC_ROOT = os.path.join(BASE_DIR, "public/dist/static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from .jwt_settings import *

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://rapidcheck.vercel.app",
]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
