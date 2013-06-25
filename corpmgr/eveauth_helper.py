import logging
from eveauth.models import Corporation, Alliance


class EveauthObjectHelper():
    def __init__(self, apikey):
        self.apikey = apikey
        self.connection = apikey.get_api_connection()
        self.alliance_list = self.connection.eve.AllianceList().alliances

    def get_alliance_from_auth(self, allianceID):
        for alliance in self.alliance_list:
            if alliance.allianceID == allianceID:
                return alliance
        return None

    def get_corporation(self, corporationID):
        try:
            corp = Corporation.objects.get(pk=corporationID)
            return corp
        except Corporation.DoesNotExist:
            corpsheet = self.connection.corp.CorporationSheet(corporationID=corporationID)
            corp = Corporation(corp_id=corporationID, name=corpsheet.corporationName)
            corp.save()
            corp.generate_logo(self.apikey)
            return corp

    def get_alliance(self, allianceID):
        try:
            alliance = Alliance.objects.get(pk=allianceID)
            return alliance
        except Alliance.DoesNotExist:
            alliance_object = self.get_alliance_from_auth(allianceID)
            alliance = Alliance(alliance_id=alliance_object.allianceID)
            alliance.alliance_name = alliance_object.allianceName
            alliance.executor = self.get_corporation(alliance_object.executorCorpID)
            alliance.save()
            return alliance

    def update_contacts_from_api(self, corporationID, allianceID):
        logger = logging.getLogger('eveauth')
        logger.info('Updating contacts from API')

        def UpdateContact(auth, contactID):
            try:
                corp = Corporation.objects.get(pk=contactID)
                return StandingsConstants.Corporation
            except Corporation.DoesNotExist:
                try:
                    corp_sheet = auth.corp.CorporationSheet(corporationID=contactID)
                    corp = Corporation(corp_id=contactID, name=corp_sheet.corporationName)
                    corp.save()
                    return StandingsConstants.Corporation
                except:
                    pass
            try:
                alliance = Alliance.objects.get(pk=contactID)
                return StandingsConstants.Alliance
            except Alliance.DoesNotExist:
                auth_alliance = self.get_alliance_from_auth(contactID)
                if auth_alliance is not None:
                    executor_corp = self.get_corporation(auth_alliance.executorCorpID)
                    alliance = Alliance(alliance_id=contactID, alliance_name=auth_alliance.name, executor=executor_corp)
                    alliance.save()
                    return StandingsConstants.Alliance
            return StandingsConstants.Character

        contact_list = self.connection.corp.ContactList()
        corp_list = contact_list.corporateContactList
        corp = self.get_corporation(corporationID)

        from models import CorporationStandingsEntry

        for contact in corp_list:
            try:
                standings_entry = CorporationStandingsEntry.objects.get(corporation=corp, contact_id=contact.contactID)
                standings_entry.standing = contact.standing
                standings_entry.save()
            except CorporationStandingsEntry.DoesNotExist:
                contact_type = UpdateContact(self.connection, contact.contactID)
                standings_entry = CorporationStandingsEntry(corporation=corp, contact_id=contact.contactID)
                standings_entry.contact_type = contact_type
                standings_entry.standing = contact.standing
                standings_entry.save()

        ids_from_api = [contact.contactID for contact in corp_list]
        ids_from_db = set(CorporationStandingsEntry.objects.values_list('contact_id', flat=True))

        obsolete_entries = ids_from_db.difference(ids_from_api)
        logger.info('Removing %s obsolete entries from CorporationStandingsEntry' % len(obsolete_entries))
        for entry in obsolete_entries:
            logger.debug('Removing contact id %s' % entry)
            corp_standings_entry = CorporationStandingsEntry.objects.get(contact_id=entry, corporation=corp)
            corp_standings_entry.delete()

        if allianceID:
            corp_alliance_list = contact_list.allianceContactList
            auth_alliance = self.get_alliance(allianceID)
            from models import AllianceStandingsEntry

            for contact in corp_alliance_list:
                try:
                    standings_entry = AllianceStandingsEntry.objects.get(alliance=auth_alliance,
                                                                         contact_id=contact.contactID)
                    standings_entry.standing = contact.standing
                except AllianceStandingsEntry.DoesNotExist:
                    contact_type = UpdateContact(self.connection, contact.contactID)
                    standings_entry = AllianceStandingsEntry(alliance=auth_alliance, contact_id=contact.contactID)
                    standings_entry.contact_type = contact_type
                    standings_entry.standing = contact.standing
                    standings_entry.save()

            ids_from_api = [contact.contactID for contact in corp_alliance_list]
            ids_from_db = set(AllianceStandingsEntry.objects.values_list('contact_id', flat=True))

            obsolete_entries = ids_from_db.difference(ids_from_api)
            logger.info('Removing %s obsolete entries from AllianceStandingsEntry' % len(obsolete_entries))
            for entry in obsolete_entries:
                logger.debug('Removing contact id %s' % entry)
                corp_standings_entry = AllianceStandingsEntry.objects.get(contact_id=entry, alliance=auth_alliance)
                corp_standings_entry.delete()


class StandingsConstants():
    Excellent = 'Excellent'
    Good = 'Good'
    Neutral = 'Neutral'
    Bad = 'Bad'
    Terrible = 'Terrible'

    Character = 'Character'
    Corporation = 'Corporation'
    Alliance = 'Alliance'

    def get_standings_string(self, standing):
        if standing == -10:
            return self.Terrible
        if standing < 0:
            return self.Bad
        if standing == 0:
            return self.Neutral
        if standing < 10:
            return self.Good
        if standing == 10:
            return self.Excellent

        return self.Neutral
