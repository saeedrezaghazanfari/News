
from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = '70e6q=hit9m@w5v!^wv_9hiluxxtnpqy9i@p)zz@k^s6enn@7+'


# DEBUG = config('DEBUG')
DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # add humanize package
    'django.contrib.humanize',

    # Packs
    'django_render_partial',
    'widget_tweaks',
    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
	'django_cleanup',
	'captcha',

    # Apss
    'News_Account.apps.NewsAccountConfig',
    'Extentions',
    'News_Pannel.apps.NewsPannelConfig',
    'News_Post.apps.NewsPostConfig',
    'News_Sitesetting.apps.NewsSitesettingConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # MiddleWares

]

ROOT_URLCONF = 'News.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # render_partial
                'django.template.context_processors.request'
            ],
        },
    },
]

WSGI_APPLICATION = 'News.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets")
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media_root")

# ## ###  #### MORE_CONFIG ####  ### ## #

# Custom User
AUTH_USER_MODEL = 'News_Account.User'

# crispy
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'peakaBOT@gmail.com'
EMAIL_HOST_PASSWORD = '1190274442saeed'

# ckeditor
CKEDITOR_UPLOAD_PATH = 'uploads/'

