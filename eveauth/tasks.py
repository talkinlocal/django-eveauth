from models import *

from celery.decorators import task
from celery.exceptions import SoftTimeLimitExceeded

@task(ignore_result=True)
def update_characters(user):
    try:
        for apikey in user.account.apikeys.all():
            Character.update_from_api(apikey)
    except SoftTimeLimitExceeded:
        for apikey in user.account.apikeys.all():
            Character.update_from_api(apikey)

update_characters.soft_time_limit="3600"
