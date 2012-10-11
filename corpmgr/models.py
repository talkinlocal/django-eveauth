from django.db import models
from eveauth.models import Corporation, Character
from account.models import Account
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import managers

class CorporationProfile(models.Model):
    corporation = models.OneToOneField(Corporation, related_name='mgmt_profile')
    manager = models.ForeignKey(User, related_name='corps_managed', unique=True)
    director_group = models.OneToOneField(Group)
    api_mask = models.IntegerField()
    reddit_required = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_add_now=True)
    last_modified = models.DateTimeField(auto_now=True)

    def has_director(self, user):
        try:
            return self.director_group in user.groups.all()
        except:
            # Safer this way.
            return False

    def get_directors(self):
        return self.director_group.users.all()

class ApplicationMixin(models.Model):
    STATUS_CHOICES = (
            -1, # REJECTED
            0, # NEW
            1, # PENDING REVIEW
            2, # APPROVED
            3, # PENDING DELETION
            )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, editable=False)
    reviewed_by = models.ForeignKey(Account, null=True, default=None, related_name='applications_reviewed')
    approved_by = models.ForeignKey(Account, null=True, default=None, related_name='applications_approved')
    rejected_by = models.ForeignKey(Account, null=True, default=None, related_name='applications_rejected')
    created_on = models.DateTimeField(auto_add_now=True)
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
    application_obj = models.GenericForeignKey('application_type', 'application_id')
    created_on = models.DateTimeField(auto_add_now=True)

class CorporationApplication(ApplicationMixin):
    character = models.OneToOneField(Character, related_name='corp_app')
    corporation = models.ForeignKey(Corporation, related_name='member_applications')
    created_by = models.ForeignKey(Account, related_name='corporation_applications')
    recommendations = generic.GenericRelation(Recommendation,
                                        content_type_field='application_type',
                                        object_id_field='application_id')

    objects = managers.CorporationAppMgr()

class AllianceApplication(ApplicationMixin):
    corporation = models.OneToOneField(Corporation, related_name='alliance_application')
    created_by = models.ForeignKey(Account, related_name='alliance_applications')
    recommendations = generic.GenericRelation(Recommendation,
                                        content_type_field='application_type',
                                        object_id_field='application_id')

    objects = managers.AllianceAppMgr()
