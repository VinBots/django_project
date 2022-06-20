import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
INSTALLED_APPS = [
    "django_crontab",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_project",
    "corporates",
    "leaderboard",
    "market",
    "accounts",
    "django.contrib.humanize",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "django_project.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "django_project"),
        ],
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
WSGI_APPLICATION = "django_project.wsgi.application"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
LOGIN_URL = "login"
# Adding ASGI Application
ASGI_APPLICATION = "django_project.routing.application"
# To use home.html as default home page
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
# Define folder location of ‘static’ folder
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_ROOT = os.path.join(BASE_DIR, "static", "django_project")

# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'django_project', 'static'),
#    ]
STATICFILES_FINDERS = [
    # "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = True

# STORAGE FOLDER STRUCTURE
STORAGE_FOLDER = os.path.join(SERVER_BASE_DIR, "storage")

DATA_FOLDER = os.path.join(STORAGE_FOLDER, "data")
EXCEL_DB_FOLDER = os.path.join(DATA_FOLDER, "excel_db")
SBTI_FOLDER = os.path.join(DATA_FOLDER, "sbti")

SUPPORTING_DOCS_FOLDER = os.path.join(STORAGE_FOLDER, "supporting_docs")

MEDIA_ROOT = SUPPORTING_DOCS_FOLDER
