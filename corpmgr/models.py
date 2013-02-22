from django.db import models
from eveauth.models import Corporation, Character, Alliance
from account.models import Account
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import managers

class CorporationProfile(models.Model):
    corporation = models.OneToOneField(Corporation, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='corps_managed', unique=True)
    director_group = models.OneToOneField(Group, related_name='directors_of')
    api_mask = models.IntegerField()
    reddit_required = models.BooleanField(default=False)
    alliance_profile = models.ForeignKey('AllianceProfile', related_name='member_corp_profiles', blank=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name='corps_allowed')

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
        if hasattr(self, 'executor_of'):
            if self.executor_of.exists():
                return True

        return False

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

    groups = models.ManyToManyField(Group, related_name='alliances_allowed')

    def __str__(self):
        return "<Alliance Profile: %s>" % (self.alliance.alliance_name,)

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
