import os
from django_project.settings.common import *
from config import Config as c

DEBUG = True

SECRET_KEY = "xx"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres2",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

BASE_DIR_LIB = os.path.join(c.DATA_FOLDER, c.LIBRARY_FOLDER)
MEDIA_ROOT = BASE_DIR_LIB
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/download/"
