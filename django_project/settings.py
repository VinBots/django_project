"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from numpy import true_divide
import netifaces

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

X_FRAME_OPTIONS = 'DENY' #'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = ''
with open('../env/secret.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Find out what the IP addresses are at run time
# This is necessary because otherwise Gunicorn will reject the connections
def ip_addresses():
    ip_list = []
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        for x in (netifaces.AF_INET, netifaces.AF_INET6):
            if x in addrs:
                ip_list.append(addrs[x][0]['addr'])
    return ip_list

#ALLOWED_HOSTS = ip_addresses()
ALLOWED_HOSTS = ['planetbonus.com', 'net0tracker.org', 'net0tracker.com', '64.227.14.214', 'www.net0tracker.com', 'www.net0tracker.org', 'www.planetbonus.com']
#ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_project',
    'channels',
    'bootstrap4',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_static_support',
    'corporates',
    'leaderboard',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Adding additional MIDDLEWARE
    'whitenoise.middleware.WhiteNoiseMiddleware',
	'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR,'templates', 'django_project')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': '7b2ad1513df1ea80797a06dd6f056a90',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# ———- Add Django Dash start ——————————–
# Adding ASGI Application
ASGI_APPLICATION = 'django_project.routing.application'
#
# To use home.html as default home page
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
# Define folder location of ‘static’ folder
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# ‘django_dash’: django app name

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'django_project', 'static'),
#    ]

# Static content of Plotly components that should
# be handled by the Django staticfiles infrastructure
PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_bootstrap_components',
    'dash_renderer',
    'dpd_components',
    'dpd_static_support',
]
# Staticfiles finders for locating dash app assets and related files (Dash static files)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]
# Channels config, to use channel layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
        },
    },
}

"""
PLOTLY_DASH = {
    "ws_route" :"dpd/ws/channel",
    "http_route":"dpd/views",
    "http_poke_enabled":True,
    "insert_demo_migrations":False,
    "cache_timeout_initial_arguments": 360,
    "view_decorator": None,
    "cache_arguments": True,
    "serve_locally": False,
    }
"""