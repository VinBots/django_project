import os
from django_project.settings.common import *

DEBUG = True

SECRET_KEY = "xx"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
