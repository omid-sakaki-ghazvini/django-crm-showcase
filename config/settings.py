"""
Django settings for config project.

Django CRM & Customer API Showcase
Author: Omid Sakaki Ghazvini
GitHub: https://github.com/omid-sakaki-ghazvini

A production-ready, bilingual (Persian/English) CRM system.
"""

import os
from pathlib import Path

# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

# ⚠️ در production این را از environment variable بخوانید
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-!@#change-this-in-production-!@#"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"] if DEBUG else os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
).split(",")


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # --- Unfold (admin theme) — باید قبل از admin باشد ---
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",

    # --- Django built-in ---
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --- Third-party ---
    "rest_framework",

    # --- Local apps ---
    "customers",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    # i18n: باید بعد از Session و قبل از Common باشد
    "django.middleware.locale.LocaleMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URLS & WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # تمپلیت‌های مشترک پروژه
        "APP_DIRS": True,                    # تمپلیت‌های داخل اپ‌ها
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # برای دسترسی به زبان جاری در همه تمپلیت‌ها
                "django.template.context_processors.i18n",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

# SQLite برای development | PostgreSQL برای production
if os.environ.get("DJANGO_USE_POSTGRES") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "crm"),
            "USER": os.environ.get("POSTGRES_USER", "crm_user"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================
# INTERNATIONALIZATION (i18n) — دوزبانه
# ============================================================

# زبان پیش‌فرض: فارسی
LANGUAGE_CODE = "fa"

# منطقه زمانی: تهران
TIME_ZONE = "Asia/Tehran"

USE_I18N = True
USE_TZ = True

# زبان‌های پشتیبانی‌شده
LANGUAGES = [
    ("fa", "فارسی"),
    ("en", "English"),
]

# مسیر فایل‌های ترجمه
LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ============================================================
# STATIC & MEDIA FILES
# ============================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}


# ============================================================
# ADMIN CUSTOMIZATION (فارسی + دوزبانه)
# ============================================================

ADMIN_SITE_HEADER = "سامانه مدیریت مشتریان"
ADMIN_SITE_TITLE = "پنل مدیریت CRM"
ADMIN_INDEX_TITLE = "به سامانه CRM خوش آمدید"


# ============================================================
# UNFOLD — Modern Admin Theme
# ============================================================

UNFOLD = {
    "SITE_TITLE": "CRM Showcase",
    "SITE_HEADER": "🚀 سامانه مدیریت مشتریان",
    "SITE_URL": "/",
    "SITE_SYMBOL": "dashboard",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": None,
    "COLORS": {
        "primary": {
            "50":  "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
    },
}


# ============================================================
# LOGGING (اختیاری — برای production)
# ============================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}