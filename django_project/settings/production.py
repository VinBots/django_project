from django_project.settings.common import *


DEBUG = True
with open("../env/secret.txt") as f:
    SECRET_KEY = f.read().strip()
ALLOWED_HOSTS = [
    "planetbonus.com",
    "net0tracker.org",
    "net0tracker.com",
    "64.227.14.214",
    "www.net0tracker.com",
    "www.net0tracker.org",
    "www.planetbonus.com",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": "7b2ad1513df1ea80797a06dd6f056a90",
        "HOST": "localhost",
        "PORT": "",
    }
}
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
