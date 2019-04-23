from .settings import *

DEBUG = False

SECRET_KEY = ''

ALLOWED_HOSTS = ['homelinks.ir']


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
