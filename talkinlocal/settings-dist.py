import os
#from pybb.settings import *


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
   ("John Doe", "anonymous@example.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "http://media.wheddit.com/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "http://media.wheddit.com/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "sanitized"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "pinax_utils.context_processors.settings",
    "account.context_processors.account",
    #"djangohelper.context_processors.ctx_config",
]


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "onlineuser.middleware.OnlineUserMiddleware",
]

ROOT_URLCONF = "wheddit.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "wheddit.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",

    # external
    "account",
    "metron",
    "south",
    "bootstrap",
    "djcelery",
    "redis",
    "celery",

    # project
    "eveauth",
    "vreddit",
    "kombu.transport.django",
    "oauth_provider",
    "pagination",
    "simpleavatar",
    "onlineuser",
    "attachments",
    "forum",
    "corpmgr",

    #Testing
    #"mumble",
    #"djextdirect",
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
#EMAIL_HOST = 'smtp.googlemail.com'
#EMAIL_PORT = 465
#EMAIL_HOST_USER = 'wheddit@gmail.com'
#EMAIL_HOST_PASSWORD = 'sanitized'
DEFAULT_FROM_EMAIL = 'admin@wheddit.com'


THEME_ACCOUNT_ADMIN_URL = 'http://beta.wheddit.com/admin'
AUTH_PROFILE_MODULE = "account.Account"
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

# Celery setup

#BROKER_URL = 'redis://'
BROKER_URL = "django://"
#BROKER_URL = "amqp://sanitized:sanitized@localhost:5672//"

#BROKER_HOST = 'localhost'
#BROKER_BACKEND = 'redis'
FORUM_USE_REDIS = True
FORUM_REDIS_PORT = 6379
FORUM_REDIS_HOST = "localhost"
#BROKER_USER = ""
#BROKER_VHOST = "0"
#REDIS_DB = 0
#REDIS_CONNECT_RETRY = True
#CELERY_SEND_EVENTS = True
#CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES = 120
#CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

#BROKER_PORT = 5672
#BROKER_USER = 'sanitized'
#BROKER_PASSWORD = 'sanitized'
#BROKER_VHOST = 'beta'

CELERY_ALWAYS_EAGER = True
CELERYD_LOG_LEVEL = 'DEBUG'

CELERY_IMPORTS = (
        "eveauth.tasks",
        "vreddit.tasks",
)

import djcelery
djcelery.setup_loader()

# Activity / metron
METRON_ACTIVITY_SESSION_KEY_NAME = "_beta_metron_activity"

METRON_SETTINGS = {
        "mixpanel": {
            "1": "55343cfca66ea221c898ac77c72bd2b6", # Beta
            "2": "", # Production
            },
        }

TUNNEL_EJABBERD_AUTH_GATEWAY_LOG = os.path.join(PROJECT_ROOT, "ejabber.log")

# Reddit stuff
REDDIT_CONFIRMATION_EXPIRE_DAYS = 10
REDDIT_LOGIN_UNIQUE = True
REDDIT_USE_OAUTH = True
REDDIT_APP_ID = 'sanitized'
REDDIT_APP_SECRET = 'sanitized'
REDDIT_USER = 'sanitized'
REDDIT_PASSWORD = 'sanitized'
REDDIT_USER_AGENT = 'Wormbro Reddit Verification Bot'
REDDIT_BOT_URL = 'http://beta.wheddit.com'
REDDIT_AUTH_SUBJECT = 'Wormbro Verification'

# Oauth Setup
OAUTH_REALM_KEY_NAME = 'http://beta.wheddit.com'

CTX_CONFIG = {}

LOGIN_URL = '/account/login'

BBCODE_AUTO_URLS = True

HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []

# forum

FORUM_STANDALONE = False
FORUM_USE_REDIS = False
FORUM_POST_FORMATTER = 'forum.formatters.BBCodeFormatter'
FORUM_USE_DEFAULT_CHAR = True

# Corp Manager

# Minimum api key mask (the bare minimum for access to SOME of our services)
EVE_CORP_MIN_MASK = 8388608
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG = "/var/django/DEV/log/jabber_bridge.log"

import logging
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG_LEVEL = logging.DEBUG


# Mumble Options
TEST_MURMUR_LAB_DIR = "/var/django/DEV/murmur"
TEST_MURMUR_FILES_DIR = "/var/django/DEV/wheddit/murmur"
DEFAULT_CONN = 'Meta:tcp -h 127.0.0.1 -p 6502'
SLICE = '/usr/share/slice/Murmur.ice'                          ##
SLICEDIR = '/usr/share/slice'                                  ##
MUMBLE_DJANGO_URL  = '/'                                       ##
MUMBLE_DJANGO_ROOT = '/var/django/DEV/wheddit'
