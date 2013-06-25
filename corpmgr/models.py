from account.models import Account
from corpmgr.tasks import update_standings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from eveauth.models import Corporation, Character, Alliance, APIKey
from eveauth_helper import EveauthObjectHelper, StandingsConstants

import managers


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
                        corporation_profile=self,
                        status__in=status,
                    )
                except:
                    apps = CorporationApplication.objects.filter(
                        corporation_profile=self,
                        status=status,
                    )

            else:
                apps = CorporationApplication.objects.filter(
                    corporation_profile=self,
                )
        return apps

    def pending_applications(self, status=None):
        apps = self.get_applications((0, 1))
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

class Coalition(models.Model):
    name = models.CharField(max_length=80, unique=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

class CoalitionProfile(models.Model):
    coalition = models.OneToOneField(Coalition, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='coalitions_managed')
    director_group = models.OneToOneField(Group, related_name='coalition_managers_of')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    def has_director(self, user):
        try:
            return self.director_group in user.groups.all()
        except:
            # Safer this way.
            return False

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='groups_managed')
    org_type = models.ForeignKey(ContentType)
    org_id = models.PositiveIntegerField()
    org_obj = generic.GenericForeignKey('org_type', 'org_id')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

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


# Signals because circular
@receiver(post_save, sender=APIKey)
def key_type_automater(sender, apikey, created, **kwargs):
    key_type = apikey.get_key_type()
    if key_type == 'Corporation':
        import sys

        conn = apikey.get_api_connection()
        corpsheet = conn.corp.CorporationSheet()
        corpID = corpsheet.corporationID
        allianceID = corpsheet.allianceID

        print >> sys.stderr, "AllianceID: %s ; CorpID: %s; Dump %s" % (allianceID, corpID, corpsheet)

        def add_alliance(allianceID, group):
            try:
                auth_alliance = Alliance.objects.get(alliance_id=allianceID)
            except Alliance.DoesNotExist:
                alliance = EveauthObjectHelper(apikey).get_alliance_from_auth(allianceID)
                executor_corp = EveauthObjectHelper(apikey).get_corporation(alliance.executorCorpID)
                auth_alliance = Alliance(
                    alliance_id=allianceID,
                    alliance_name=corpsheet.allianceName,
                    executor=executor_corp
                )

            auth_alliance.save()
            try:
                alliance_profile = AllianceProfile.objects.get(alliance=auth_alliance)
            except AllianceProfile.DoesNotExist:
                alliance_profile = AllianceProfile(
                    alliance=auth_alliance,
                    manager=apikey.account.user,
                    director_group=group,
                    api_mask=None,
                )

            alliance_profile.save()
            return alliance_profile

        auth_corp = None
        try:
            auth_corp = Corporation.objects.get(pk=corpID)

        except Corporation.DoesNotExist:
            auth_corp = Corporation(corp_id=corpID, name=corpsheet.corporationName)
            auth_corp.save()
            auth_corp.generate_logo(apikey)

        try:
            corp_profile = CorporationProfile.objects.get(corporation=auth_corp)

        except CorporationProfile.DoesNotExist:
            group_name = "%s directors" % (auth_corp.name,)
            group = None
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group(name=group_name)
                group.save()
            corp_profile = CorporationProfile(
                corporation=auth_corp,
                manager=apikey.account.user,
                director_group=group,
                api_mask=8,
                reddit_required=False,
                alliance_profile=None,
            )
            group.user_set.add(apikey.account.user)
            group.save()

            if allianceID:
                alliance_profile = add_alliance(allianceID, group)
                corp_profile.alliance_profile = alliance_profile

            corp_profile.save()

        update_standings.delay(apikey, corpID, allianceID)
