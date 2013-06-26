from celery import task
from celery.exceptions import SoftTimeLimitExceeded
from eveauth_helper import EveauthObjectHelper


@task(ignore_result=True)
def update_standings(instance, corpID, allianceID):
    print 'updating standings', corpID, allianceID
    try:
        EveauthObjectHelper(instance).update_contacts_from_api(corpID, allianceID)
    except SoftTimeLimitExceeded:
        print('Time limit exceeded')
        pass
    except:
        import sys
        print sys.exc_info()[1]


@task(ignore_result=True)
def update_all_standings():
    print('updating all standings')
    from eveauth.models import APIKey

    all_keys = APIKey.objects.all()
    for key in all_keys:
        if key.get_key_type() != "Corporation":
            continue
        api_connection = key.get_api_connection()
        corpsheet = api_connection.corp.CorporationSheet()
        corp_id = corpsheet.corporationID
        alliance_id = corpsheet.allianceID
        print("%s %s %s" % (api_connection, corp_id, alliance_id))
        update_standings(key, corp_id, alliance_id)


update_standings.soft_time_limit = 3600
