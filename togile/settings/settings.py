"""
Django settings for togile project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4h#*p9u-zm1(64fbo#3=)cfv#%bl5$vus9pz7x%n-+tjlsnn6c'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'south',
    'tastypie',
    'togile.apps.todo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'togile.urls'

WSGI_APPLICATION = 'togile.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if 'TOGILE_PRODUCTION' not in os.environ:

    DEBUG = True
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'todos.db'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
APP_URL = '/app/'
APP_PATH = os.path.join(BASE_DIR, 'frontend', 'app')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'frontend', 'app'),
# )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# AUTH & SOCIAL AUTH
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_LOGIN_URL = '/login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'

FRONTEND_APP_INDEX = APP_URL + 'index.html'
FRONTEND_APP_LISTS = APP_URL + 'index.html#/lists'

if 'TOGILE_PRODUCTION' in os.environ:
    from prod_settings import *  # NOQA
else:
    try:
        from local_settings import *  # NOQA
    except ImportError:
        pass
