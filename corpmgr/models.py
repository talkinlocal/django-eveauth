from django.db import models
from eveauth.models import Corporation, Character, Alliance, APIKey
from account.models import Account
from tasks import update_standings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import managers

from django.db.models.signals import post_save
from django.dispatch import receiver

class CorporationProfile(models.Model):
    corporation = models.OneToOneField(Corporation, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='corps_managed', unique=True)
    director_group = models.OneToOneField(Group, related_name='directors_of')
    api_mask = models.IntegerField()
    reddit_required = models.BooleanField(default=False)
    alliance_profile = models.ForeignKey('AllianceProfile', related_name='member_corp_profiles', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ( 'corporation', 'alliance_profile' )

    def has_director(self, user):
        try:
            return self.director_group in user.groups.all()
        except:
            # Safer this way.
            return False

    def get_directors(self):
        return self.director_group.users.all()

    def is_alliance(self):
        if hasattr(self.corporation, 'executor_of'):
            if self.corporation.executor_of.exists():
                return True

        return False

    def get_applications(self, status=None):
        apps = []
        if hasattr(self, 'member_applications'):
            if status is not None:
                try:
                    apps = CorporationApplication.objects.filter(
                            corporation_profile = self,
                            status__in = status,
                            )
                except:
                    apps = CorporationApplication.objects.filter(
                            corporation_profile = self,
                            status = status,
                            )

            else:
                apps = CorporationApplication.objects.filter(
                        corporation_profile = self,
                        )
        return apps

    def pending_applications(self, status=None):
        apps = self.get_applications((0,1))
        return apps

    def standings_with(self, contactID):
        try:
            standings_entry = CorporationStandingsEntry.objects.get(corporation=self.corporation, contact_id=contactID)
            return (standings_entry.standing, StandingsConstants().get_standings_string(standings_entry.standing))
        except CorporationStandingsEntry.DoesNotExist:
            return (0, StandingsConstants.Neutral)

    def __str__(self):
        return "<Corporation Profile: %s>" % (self.corporation.name,)

    def __unicode__(self):
        return self.corporation.name

class AllianceProfile(models.Model):
    alliance = models.OneToOneField(Alliance, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='alliances_managed')
    director_group = models.OneToOneField(Group, related_name='executive_directors_of')
    api_mask = models.IntegerField(blank=True, null=True, default=None)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Alliance Profile: %s>" % (self.alliance.alliance_name,)

    def has_director(self, user):
        try:
            return self.director_group in user.groups.all()
        except:
            # Safer this way.
            return False

    def standings_with(self, contactID):
        try:
            standings_entry = AllianceStandingsEntry.objects.get(alliance=self.alliance, contact_id=contactID)
            return (standings_entry.standing, StandingsConstants().get_standings_string(standings_entry.standing))
        except AllianceStandingsEntry.DoesNotExist:
            return (0, StandingsConstants.Neutral)

#class Coalition(models.Model):
#    name = models.CharField(max_length=80, unique=True)
#    created_on = models.DateTimeField(auto_now_add=True, editable=False)
#    last_modified = models.DateTimeField(auto_now=True)

#class CoalitionProfile(models.Model):
#    coalition = models.OneToOneField(Coalition, related_name='mgmt_profile')
#    manager = models.ForeignKey(User, related_name='coalitions_managed')
#    director_group = models.OneToOneField(Group, related_name='coalition_managers_of')
#    created_on = models.DateTimeField(auto_now_add=True, editable=False)
#    last_modified = models.DateTimeField(auto_now=True)
#
#    def has_director(self, user):
#        try:
#            return self.director_group in user.groups.all()
#        except:
#            # Safer this way.
#            return False

#class GroupProfile(models.Model):
#    group = models.OneToOneField(Group, related_name='mgmt_profile')
#    manager = models.ForeignKey(User, related_name='groups_managed')
#    org_type = models.ForeignKey(ContentType)
#    org_id = models.PositiveIntegerField()
#    org_obj = generic.GenericForeignKey('org_type', 'org_id')
#    created_on = models.DateTimeField(auto_now_add=True, editable=False)
#    last_modified = models.DateTimeField(auto_now=True)

class ApplicationMixin(models.Model):
    REJECTED = -1
    NEW = 0
    PENDING = 1
    APPROVED = 2
    PURGE = 3
    STATUS_CHOICES = (
            (REJECTED, 'Rejected'),
            (NEW, 'New'),
            (PENDING, 'Pending Review'),
            (APPROVED, 'Approved'),
            (PURGE, 'Pending Deletion'),
            )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def reject(self):
        self.status = -1
        self.save()

    def pending(self):
        self.status = 1
        self.save()

    def approve(self):
        self.status = 2
        self.save()

    def mark_delete(self):
        self.status = 3
        self.save()

    def is_approved(self):
        return self.status == 2

    def is_pending(self):
        return self.status == 1

    def is_rejected(self):
        return self.status == -1

    def status_text(self):
        for status in self.STATUS_CHOICES:
            if status[0] is self.status:
                return status[1]

        return 'Unknown'

class Recommendation(models.Model):
    account = models.ForeignKey(Account, related_name='app_recommendations')
    application_type = models.ForeignKey(ContentType)
    application_id = models.PositiveIntegerField()
    application_obj = generic.GenericForeignKey('application_type', 'application_id')
    created_on = models.DateTimeField(auto_now_add=True)

class CorporationApplication(ApplicationMixin):
    character = models.OneToOneField(Character, related_name='corp_app')
    corporation_profile = models.ForeignKey(CorporationProfile, related_name='member_applications')
    created_by = models.ForeignKey(Account, related_name='corporation_applications')
    recommendations = generic.GenericRelation(Recommendation,
                                        content_type_field='application_type',
                                        object_id_field='application_id')
    reviewed_by = models.ForeignKey(Account, null=True, default=None, related_name='mbr_applications_reviewed')
    approved_by = models.ForeignKey(Account, null=True, default=None, related_name='mbr_applications_approved')
    rejected_by = models.ForeignKey(Account, null=True, default=None, related_name='mbr_applications_rejected')

    objects = managers.CorporationAppMgr()

    class Meta:
        unique_together = ('character', 'corporation_profile')

    def get_reddit(self):
        if self.corporation_profile.reddit_required:
            account = self.character.account
            reddit_account = account.reddit_account
            return reddit_account

        return None

    def __unicode__(self):
        return u"%s application for %s" % (self.corporation_profile, self.character)

class AllianceApplication(ApplicationMixin):
    corporation = models.OneToOneField(Corporation, related_name='alliance_application', unique=True)
    created_by = models.ForeignKey(Account, related_name='alliance_applications')
    recommendations = generic.GenericRelation(Recommendation,
                                        content_type_field='application_type',
                                        object_id_field='application_id')

    reviewed_by = models.ForeignKey(Account, null=True, default=None, related_name='crp_applications_reviewed')
    approved_by = models.ForeignKey(Account, null=True, default=None, related_name='crp_applications_approved')
    rejected_by = models.ForeignKey(Account, null=True, default=None, related_name='crp_applications_rejected')
    objects = managers.AllianceAppMgr()

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

class CorporationStandingsEntry(models.Model):
    corporation = models.ForeignKey(Corporation)
    contact_type = models.CharField(max_length=12)
    standing = models.DecimalField(max_digits=3, decimal_places=1)
    contact_id = models.IntegerField()

class AllianceStandingsEntry(models.Model):
    alliance = models.ForeignKey(Alliance)
    contact_type = models.CharField(max_length=12)
    standing = models.DecimalField(max_digits=3, decimal_places=1)
    contact_id = models.IntegerField()

class EveauthObjectHelper():
    def __init__(self, instance):
        self.connection = instance.get_api_connection()
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
            corp.generate_logo(self.instance)
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
        print 'update_contacts_from_api'
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
                    alliance = Alliance(alliance_id = contactID, alliance_name = auth_alliance.name, executor = executor_corp)
                    alliance.save()
                    return StandingsConstants.Alliance
            return StandingsConstants.Character

        contact_list = self.connection.corp.ContactList()
        corp_list = contact_list.corporateContactList
        corp = self.get_corporation(corporationID)

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

        if allianceID:
            corp_alliance_list = contact_list.allianceContactList
            auth_alliance = self.get_alliance(allianceID)
            for contact in corp_alliance_list:
                try:
                    standings_entry = AllianceStandingsEntry.objects.get(alliance=auth_alliance, contact_id = contact.contactID)
                    standings_entry.standing = contact.standing
                except AllianceStandingsEntry.DoesNotExist:
                    contact_type = UpdateContact(self.connection, contact.contactID)
                    standings_entry = AllianceStandingsEntry(alliance=auth_alliance, contact_id=contact.contactID)
                    standings_entry.contact_type = contact_type
                    standings_entry.standing = contact.standing
                    standings_entry.save()

# Signals because circular
@receiver(post_save, sender=APIKey)
def key_type_automater(sender, instance, created, **kwargs):
    key_type = instance.get_key_type()
    if key_type == 'Corporation':
        import sys
        conn = instance.get_api_connection()
        corpsheet = conn.corp.CorporationSheet()
        corpID = corpsheet.corporationID
        allianceID = corpsheet.allianceID

        print >> sys.stderr, "AllianceID: %s ; CorpID: %s; Dump %s" % (allianceID, corpID, corpsheet)

        def add_alliance(allianceID, group):
            try:
                auth_alliance = Alliance.objects.get(alliance_id = allianceID)
            except Alliance.DoesNotExist:
                alliance = EveauthObjectHelper(conn).get_alliance_from_auth(allianceID)
                executor_corp = EveauthObjectHelper(conn).get_corporation(alliance.executorCorpID)
                auth_alliance = Alliance(
                                    alliance_id = allianceID,
                                    alliance_name = corpsheet.allianceName,
                                    executor = executor_corp
                                )

            auth_alliance.save()
            try:
                alliance_profile = AllianceProfile.objects.get(alliance = auth_alliance)
            except AllianceProfile.DoesNotExist:
                alliance_profile = AllianceProfile(
                        alliance = auth_alliance,
                        manager = instance.account.user,
                        director_group = group,
                        api_mask = None,
                        )

            alliance_profile.save()
            return alliance_profile

        auth_corp = None
        try:
            auth_corp = Corporation.objects.get(pk=corpID)

        except Corporation.DoesNotExist:
            auth_corp = Corporation(corp_id=corpID,name=corpsheet.corporationName)
            auth_corp.save()
            auth_corp.generate_logo(instance)

        try:
            corp_profile = CorporationProfile.objects.get(corporation=auth_corp)

        except CorporationProfile.DoesNotExist:
            group_name = "%s directors" % (auth_corp.name,)
            new_group = Group(name=group_name)
            new_group.save()
            corp_profile = CorporationProfile(
                        corporation = auth_corp,
                        manager = instance.account.user,
                        director_group = new_group,
                        api_mask = 8,
                        reddit_required = False,
                        alliance_profile = None,
                    )
            new_group.user_set.add(instance.account.user)
            new_group.save()

            if allianceID:
                alliance_profile = add_alliance(allianceID,new_group)
                corp_profile.alliance_profile = alliance_profile

            corp_profile.save()
        update_standings.delay(instance, corpID, allianceID)
