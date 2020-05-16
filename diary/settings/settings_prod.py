from .settings_base import *  # noqa

import os

MARKDOWN_LOCATION = 'diary-old/entries'

DEBUG = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60  # One hour.
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

ALLOWED_HOSTS = ['diary.dport.me', '127.0.0.1', '0.0.0.0', 'localhost']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"mine": {"format": "%(levelname)s %(asctime)s %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "mine",
        }
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
}
