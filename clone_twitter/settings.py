from pathlib import Path
import os

# ----------------------------------
# BASE DIRECTORY
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------
# SECRET KEY e DEBUG
# ----------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key")
DEBUG = False  # Sempre False em produção

# ----------------------------------
# Hosts e CSRF
# ----------------------------------
ALLOWED_HOSTS = ["clone-twitter-n3cm.onrender.com"]  # Substitua pelo seu domínio Render
CSRF_TRUSTED_ORIGINS = [
    "https://clone-twitter-n3cm.onrender.com",
]

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
    "django_extensions",
    "users",
    "tweets",
]

AUTH_USER_MODEL = 'users.User'

# ----------------------------------
# MIDDLEWARE
# ----------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
# DATABASE (SQLite por enquanto)
# ----------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ⚠️ Se quiser persistência real, use PostgreSQL:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_DB"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": os.environ.get("POSTGRES_HOST"),
#         "PORT": os.environ.get("POSTGRES_PORT", 5432),
#     }
# }

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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------
# STATIC FILES
# ----------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic vai gerar aqui no Render

# ----------------------------------
# MEDIA FILES (Avatars, uploads)
# ----------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------
# DEFAULT AUTO FIELD
# ----------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------
# LOGIN / LOGOUT REDIRECTS
# ----------------------------------
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"       # Após login bem-sucedido
LOGOUT_REDIRECT_URL = "/users/login/"

# ----------------------------------
# OBSERVAÇÕES IMPORTANTES PARA DEPLOY
# ----------------------------------
# 1. Antes de rodar no Render, rode: python manage.py collectstatic --noinput
# 2. Gunicorn será usado como servidor: gunicorn clone_twitter.wsgi
# 3. SQLite funciona, mas alterações no container não são persistentes. Para produção real, use PostgreSQL.
# 4. Variáveis sensíveis (SECRET_KEY, DB credentials) devem ser configuradas no Render → Environment → Environment Variables
