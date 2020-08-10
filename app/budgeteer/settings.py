"""
Django settings for budgeteer project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Credits https://stackoverflow.com/a/49395080
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

# Application definition
INSTALLED_APPS = [
    # Address https://code.djangoproject.com/ticket/20372
    # Declaration order: own app -> 3rd party -> django builtins
    'budgets',
    'rest_framework',
    # Not using the admin panel atm
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
if 'y' in os.getenv("DJANGO_DEBUG_MODE"):
    DEBUG = True

    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    # IPS able to see debug tools inside views
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

    DEBUG_TOOLBAR_PANELS = [
      'debug_toolbar.panels.versions.VersionsPanel',
      'debug_toolbar.panels.timer.TimerPanel',
      'debug_toolbar.panels.settings.SettingsPanel',
      'debug_toolbar.panels.headers.HeadersPanel',
      'debug_toolbar.panels.request.RequestPanel',
      'debug_toolbar.panels.sql.SQLPanel',
      'debug_toolbar.panels.staticfiles.StaticFilesPanel',
      'debug_toolbar.panels.templates.TemplatesPanel',
      'debug_toolbar.panels.cache.CachePanel',
      'debug_toolbar.panels.signals.SignalsPanel',
      'debug_toolbar.panels.logging.LoggingPanel',
      'debug_toolbar.panels.redirects.RedirectsPanel',
      'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    RENDER_PANELS = True
else:
    DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [os.getenv("SITENAME")]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}

ROOT_URLCONF = 'budgeteer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'budgeteer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASE_TYPE = os.environ.get("DATABASE", default=False)
if DATABASE_TYPE:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE"),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# NOTE: avoding the leading slash will lookup the url in the app *where the user during login/logout*
# Converesly, using a leading slash, will tell django wich namespace to use
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'
