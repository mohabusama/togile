"""
togile project

Production Settings. Modify to suit your production environment.
"""

# Disable Debugging
DEBUG = False
TEMPLATE_DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# Secret Key - Generate A new Secret for your Production Env
SECRET_KEY = '@-I_e+M0!bN*j~~B<ka"bC8ss2Fpi9bk_YE_.wV2*aHa7CZW5vW'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'togile',
        'USER': 'togile',
        'PASSWORD': 'togileS3kr3teer',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Memcached as Default Production cache!
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

STATIC_ROOT = '%(static)s'
