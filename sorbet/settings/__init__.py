import sys
from os.path import dirname, realpath, join, normpath
from celery.schedules import crontab
import djcelery
djcelery.setup_loader()

SITE_ROOT = join(dirname(realpath(__file__)), '../../')
sys.path.insert(0, normpath(join(SITE_ROOT, "sorbet/")))


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


MEDIA_ROOT = join(SITE_ROOT, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


SECRET_KEY = 'v3qameh$9l3-oor&amp;fjtrpc=2uxf3t1u0$xl4b2k_1(=hz0k_wc'
ROOT_URLCONF = 'sorbet.urls'
WSGI_APPLICATION = 'sorbet.wsgi.application'
ADMINS = [('Isaac Bythewood', 'isaac@bythewood.me'),
          ('Krzysztof Klimonda', 'kklimonda@syntaxhighlighted.com')]
MANAGERS = ADMINS
LOGIN_REDIRECT_URL = '/feeds/'
PROJECT_APPS = (
    'sorbet.core',
    'sorbet.feedmanager',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jenkins',
    'gunicorn',
    'compressor',
    'south',
    'djcelery',
    'core',
    'feedmanager',
    'vendor'
)

AUTHENTICATION_BACKENDS = ['sorbet.core.backends.EmailAuthBackend']
AUTH_PROFILE_MODULE = 'core.UserProfile'

INVITE_ONLY = True
INVITES_PER_WEEK = 50
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    "send-invitations": {
        "task": "core.tasks.send_invitations",
        "schedule": crontab(hour=0, minute=0, day_of_week="monday"),
        "args": (INVITES_PER_WEEK,),
    },
    "update-feeds": {
        "task": "feedmanager.tasks.send_updates",
        "schedule": timedelta(hours=3),
    }
}
