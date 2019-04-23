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


SECRET_KEY = "ja$(a6%6&s%_w$w!zvag94$8^z^2sk3(fak@)2-0ws3ufafx*38#i^4gg41us#$%os22!1k59v6*6bxYQ"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homelink_homelinks',
        'USER': 'homelink_user',
        'PASSWORD': '7ujPaYn5+-jy',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Rechapcha
RECAPTCHA_PRIVATE_KEY = '6LfgHp4UAAAAAH-WnmcVPsG9MLKihnKmM8koeOfQ'
RECAPTCHA_PUBLIC_KEY = '6LfgHp4UAAAAAMEo5U5lHaHcFTMSJNysmG1QU0gt'


# Email
EMAIL_BACKEND = ''
