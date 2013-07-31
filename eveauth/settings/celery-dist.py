import djcelery
from datetime import timedelta

# Celery setup
BROKER_URL = "django://"
# CELERY_RESULT_BACKEND = "django://"
CELERY_TASK_RESULT_EXPIRES = 120
CELERY_ALWAYS_EAGER = False
CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = (
    "eve_auth.tasks",
    "vreddit.tasks",
    "corpmgr.tasks",
)
CELERYBEAT_SCHEDULE = {
    'update-standings': {
        'task': 'corpmgr.tasks.update_all_standings',
        'schedule': timedelta(minutes=60),
    },
    'process-reddit-queue': {
        'task': 'vreddit.tasks.process_reddit_queue',
        'schedule': timedelta(minutes=5),
    },
}

djcelery.setup_loader()
