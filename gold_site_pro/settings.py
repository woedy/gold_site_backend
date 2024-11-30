"""
Django settings for gold_site_pro project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+jmzw&)$6njrw)8l1e5t^x3y(-sa@pd$spdb3u89zxrt+x3(xy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'etornamasamoah@gmail.com'
EMAIL_HOST_PASSWORD = 'vhixgmqnlwkbsgzv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'SwapWing <samahatbarter@gmail.com>'
BASE_URL = '0.0.0.0:80'

# Application definition

INSTALLED_APPS = [
            "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        'channels',

            'rest_framework',
    'rest_framework.authtoken',

        'corsheaders',

    'accounts',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

            'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'gold_site_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'gold_site_pro.wsgi.application'
ASGI_APPLICATION = "gold_site_pro.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'god_blass_postgres',
#         'USER': 'god_blass_postgres',
#         'PASSWORD': 'god_blass_postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#      }
# }


CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_proj")
]


STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", 'media_root')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





from celery import Celery
app = Celery('gold_site_pro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}





CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_CREDENTIALS = True



#REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'rest_framework_simplejwt.authentication.JWTAuthentication',
#        # Add other authentication classes as needed
#    ),
#}




#SIMPLE_JWT = {
#    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#}



SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')






#CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Adjust if necessary
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#CELERY_TIMEZONE = 'UTC'  # Adjust the timezone if needed