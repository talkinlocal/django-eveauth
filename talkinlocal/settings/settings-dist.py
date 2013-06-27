import os
import sys


PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.dirname(PACKAGE_ROOT))

# TODO: I would like to change this so that talkinlocal/apps is a package, but it requires touching
# nearly every file, which I'm not quite ready to do at this time
sys.path.insert(0, os.path.join(PACKAGE_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PACKAGE_ROOT, 'libs'))

# TODO: Set this to 'False' before deployment
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    ("John Doe", "anonymous@example.com"),
]

MANAGERS = ADMINS

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
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
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

ROOT_URLCONF = "talkinlocal.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "talkinlocal.wsgi.application"

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

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

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

# Activity / metron
METRON_ACTIVITY_SESSION_KEY_NAME = "_beta_metron_activity"

METRON_SETTINGS = {
    "mixpanel": {
        "1": "55343cfca66ea221c898ac77c72bd2b6",  # Beta
        "2": "",  # Production
    },
}

# Praw settings (reddit)
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