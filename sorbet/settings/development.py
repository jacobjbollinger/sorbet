from sorbet.settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(SITE_ROOT, 'development.db'),
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sorbet'
    }
}


MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
