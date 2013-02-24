from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.dispatch import receiver
from eveauth import APIKey,Corporation,Alliance
from models import CorporationProfile,AllianceProfile

@receiver(post_save, sender=APIKey)
def key_type_automater(sender, instance, created, **kwargs):
    key_type = instance.get_key_type()
    if key_type is u'Corporation':
        conn = instance.get_api_connection()
        corpsheet = conn.corp.CorporationSheet()
        corpID = corpsheet.corporationID
        if hasattr('allianceID', corpsheet):
            allianceID = corpsheet.allianceID
        try:
            auth_corp = Corporation.objects.get(pk=corpID)
        except Corporation.DoesNotExist:
            auth_corp = Corporation(corp_id=corpID,name=corpsheet.corporationName)
            auth_corp.save().generate_logo(instance)
        
        try:
            corp_profile = CorporationProfile.objects.get(corporation=auth_corp)
        except CorporationProfile.DoesNotExist:
            corp_profile = CorporationProfile(
                        corporation = auth_corp,
                        manager = instance.account.user,
                        director_group = models.Group("%s directors" % (auth_corp.name,)).save(),
                        api_mask = 8,
                        reddit_required = False,
                        alliance_profile = None,
                    )
        if allianceID:
            try:
                auth_alliance = Alliance.objects.get(alliance_id = allianceID)
            except Alliance.DoesNotExist:
                # TODO: ACTUALLY discover the executor; likely easier done with the djangokb api handler.
                auth_alliance = Alliance(
                                    alliance_id = allianceID,
                                    alliance_name = corpsheet.allianceName,
                                    executor = auth_corp
                                )

            auth_alliance.save()
            corp_profile.alliance_profile = auth_alliance
            corp_profile.save()
