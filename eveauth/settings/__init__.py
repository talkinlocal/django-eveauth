from split_settings.tools import optional, include

include(
    'settings-dist.py',
    'database-dist.py',
    'celery-dist.py',
    'logging-dist.py',
    'email-dist.py',
    'apps-dist.py',

    optional('settings.py'),
    optional('database.py'),
    optional('celery.py'),
    optional('logging.py'),
    optional('email.py'),
    optional('apps.py'),


    scope=locals()
)