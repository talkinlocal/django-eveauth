import models
from celery.decorators import task
from celery.exceptions import SoftTimeLimitExceeded

@task(ignore_result=True)
def update_standings(conn, corpID, allianceID):
    print 'updating standings', corpID, allianceID
    try:
        models.EveauthObjectHelper(conn).update_contacts_from_api(corpID, allianceID)
    except SoftTimeLimitExceeded:
        pass
    except:
        import sys
        print sys.exc_info()[1]

update_standings.soft_time_limit=3600
