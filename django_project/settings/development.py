import os
from django_project.settings.common import *

# from django_project.settings.common import LOG_FILEPATH

DEBUG = True

SECRET_KEY = "xx"

with open("../env/db_pwd.txt") as f:
    DB_PWD = f.read().strip()

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres2",
        "USER": "postgres",
        "PASSWORD": DB_PWD,
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# MEDIA_ROOT = BASE_DIR_LIB
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/download/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} message in {module} at {asctime}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOG_FILEPATH,
            "formatter": "verbose",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}
