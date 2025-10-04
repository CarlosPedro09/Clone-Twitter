from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ----------------------------------
# BASE DIRECTORY
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------
# SECRET KEY e DEBUG
# ----------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ----------------------------------
# Hosts e CSRF
# ----------------------------------
ALLOWED_HOSTS = ["clone-twitter-n3cm.onrender.com", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://clone-twitter-n3cm.onrender.com"]

# ----------------------------------
# INSTALLED APPS
# ----------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "tweets",
    "cloudinary",
    "cloudinary_storage",  # ✅ Adiciona integração de storage
]

# Modelo de usuário customizado
AUTH_USER_MODEL = "users.User"

# ----------------------------------
# MIDDLEWARE
# ----------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------------
# URLS
# ----------------------------------
ROOT_URLCONF = "clone_twitter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "clone_twitter.wsgi.application"

# ----------------------------------
# DATABASE
# ----------------------------------
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }

# ----------------------------------
# PASSWORD VALIDATORS
# ----------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------------
# LANGUAGE & TIMEZONE
# ----------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ----------------------------------
# STATIC FILES
# ----------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------------
# MEDIA FILES (Cloudinary)
# ----------------------------------
# ⚙️ Se Cloudinary estiver configurado, ele será usado para armazenar os uploads.
# Localmente, ainda usa pasta /media para facilitar testes.

if DEBUG:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    MEDIA_URL = "https://res.cloudinary.com/" + os.environ.get("CLOUDINARY_CLOUD_NAME", "") + "/image/upload/"
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ----------------------------------
# CLOUDINARY CONFIG
# ----------------------------------
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

# ----------------------------------
# LOGIN / LOGOUT REDIRECTS
# ----------------------------------
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/users/login/"

# ----------------------------------
# DEFAULT AUTO FIELD
# ----------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
