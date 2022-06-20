from django_project.settings.common import *


DEBUG = True
with open("../env/secret.txt") as f:
    SECRET_KEY = f.read().strip()

with open("../env/db_pwd.txt") as f:
    DB_PWD = f.read().strip()

ALLOWED_HOSTS = [
    "planetbonus.com",
    "net0tracker.org",
    "net0tracker.com",
    "64.227.14.214",
    "www.net0tracker.com",
    "www.net0tracker.org",
    "www.planetbonus.com",
]
old_pwd = "7b2ad1513df1ea80797a06dd6f056a90"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": DB_PWD,
        "HOST": "localhost",
        "PORT": "",
    }
}
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

MEDIA_URL = "/download/"

LOG_FOLDER = os.path.join(STORAGE_FOLDER, "log")
# LOG_FILEPATH = os.path.join(LOG_FOLDER, "debug.log")

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} message in {module} at {asctime}: {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "file": {
#             "level": "WARNING",
#             "class": "logging.FileHandler",
#             "filename": LOG_FILEPATH,
#             "formatter": "verbose",
#         },
#         "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
#     },
#     "root": {
#         "handlers": ["file", "console"],
#         "level": "INFO",
#     },
# }
