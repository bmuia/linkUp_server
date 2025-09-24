from pathlib import Path
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import timedelta
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
MODE = os.getenv("MODE", "development")

DEBUG = MODE == "development"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "channels",
    'corsheaders',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "server.wsgi.application"
ASGI_APPLICATION = "server.asgi.application"

# --- PostgreSQL ---
if MODE == "production":
    DATABASES = {"default": dj_database_url.config(default=os.getenv("POSTGRES_DATABASE_URL"))}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "mydb"),
            "USER": os.getenv("POSTGRES_USER", "myuser"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "mypassword"),
            "HOST": os.getenv("POSTGRES_HOST", "postgres"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# --- MongoDB ---
if MODE == "production":
    MONGO_URI = os.getenv("MONGO_DATABASE_URI")
    mongo_client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    mongo_db = mongo_client[os.getenv("MONGO_DB_NAME", "chat_db_prod")]
else:
    MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "mongoadmin")
    MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "mongopass")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chat_db")
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB_NAME]

MONGO_DB = mongo_db

# --- Redis (Channels) ---
if MODE == "production":
    REDIS_URL = os.getenv("REDIS_URL")
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("redis", 6379)], 
            },
        },
    }

# --- JWT ---
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.CustomUser"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



