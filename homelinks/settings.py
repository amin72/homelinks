###
# Change settings for production
###

from .dev_settings import *

DEBUG = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'crispy_forms',
    'jalali_date',
    'taggit',
    'taggit_helpers',
    'snowpenguin.django.recaptcha3',
    'axes',

    # apps
    'links.apps.LinksConfig',
    'dashboard.apps.DashboardConfig',
    'contact.apps.ContactConfig',
    'i18n_switcher.apps.I18NSwitcherConfig',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware', # must be the first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # must be the last
]


ALLOWED_HOSTS = ['homelinks.ir']
INTERNAL_IPS = []


SECRET_KEY = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Rechapcha
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_PUBLIC_KEY = ''


# Email
EMAIL_BACKEND = ''
