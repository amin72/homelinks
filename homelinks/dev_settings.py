import os
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eo+8*-a+j_!4hb@(gvt%9t^)k6ni3*j%k-k32qwgaf)hx-=%0w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.56.1', '192.168.57.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'debug_toolbar',
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
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # must be the last
]

ROOT_URLCONF = 'homelinks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'homelinks.context_processors.object_counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'homelinks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homelinks',
        'USER': 'homelink_user',
        'PASSWORD': 'homelink_user',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'public_html', 'static')

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'public_html', 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

# CRISPY
CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_REDIRECT_URL = 'dashboard:index'
LOGIN_URL = 'dashboard:login'


RECAPTCHA_PRIVATE_KEY = '6Lc6fZkUAAAAAE8c3ckrYu7FsngZ5-U_J-W6s3uJ'
RECAPTCHA_PUBLIC_KEY = '6Lc6fZkUAAAAAK6Tgha7LMhxPNZb8NopjEKbOCMZ'
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5


handler404 = 'homelinks.views.handler404'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

AXES_CACHE = 'axes_cache'
AXES_FAILURE_LIMIT = 5
AXES_LOCKOUT_TEMPLATE = 'dashboard/login.html'
AXES_COOLOFF_TIME = timedelta(minutes=5)


# Custom User Model
AUTH_USER_MODEL = 'dashboard.User'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'support@homelinks.ir'

INTERNAL_IPS = ['127.0.0.1', '::1']


LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]


REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'dashboard.api.serializers.UserDetailSerializer',
}
