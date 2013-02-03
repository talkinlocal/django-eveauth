from django.db import models
from django.conf import settings
from account.models import Account
import eveapi, os, Image, managers

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

class APIKey(models.Model):
    account = models.ForeignKey(Account, related_name='apikeys')
    api_id = models.IntegerField(primary_key=True, unique=True, help_text="The number ID of your API key")
    vcode = models.CharField(max_length=255, help_text="The verification code of your API key")
    date_added = models.DateTimeField(default=timezone.now)

    def get_characters(self):
        if hasattr(self, 'characters'):
            return self.characters.all()

    def get_formatted_characters(self):
        return ", ".join([char.__str__() for char in self.get_characters()])
    get_formatted_characters.short_description = "Characters"

    def get_key_mask(self):
        api = eveapi.EVEAPIConnection()
        eve_auth = api.auth(keyID=self.api_id, vCode=self.vcode)

        try:
            keyinfo = eve_auth.account.APIKeyInfo()
        except:
            # Welp
            pass

        access_mask = keyinfo.key.accessMask

        return access_mask

    def __unicode__(self):
        return u"%s - %s (added %s)" % ( self.api_id, self.vcode, self.date_added) 

    def __str__(self):
        return str(self.__unicode__())

class UserJID(models.Model):
    site_user = models.OneToOneField(User, related_name='jid', primary_key=True)
    node = models.CharField(max_length=256, null=False, blank=False)
    domain = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        unique_together = ('node', 'domain')

    def asJID(self):
        return u'%s@%s' % (self.node, self.domain)

    @classmethod
    def fromJID(cls, jid):
        try:
            node, domain = jid.split(u'@')
            domain = domain.split(u'/')[0]
            return cls.objects.get(node=node, domain=domain)
        except cls.DoesNotExist:
            # check if there's a matching (ish) username if configured to do so
            if hasattr(settings, 'EVE_DEFAULT_JABBER_DOMAIN'):
                if domain == settings.EVE_DEFAULT_JABBER_DOMAIN:
                    # Just in case...
                    try:
                        user = User.objects.get(username__iexact=node)
                    except User.DoesNotExist:
                        # because they asked for a THIS dang it!
                        return cls.objects.get(node=user.username.lower(), domain=domain)
                    
                    # Create one
                    return cls(node=user.username.lower(), domain=domain)

            else:
                raise cls.DoesNotExist()


class Corporation(models.Model):
    corp_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128, help_text="Corporation name")
    ticker = models.CharField(max_length=8, help_text="Corporation ticker", blank=True, default="")

    def generate_logo(self, api_key):
        api = eveapi.EVEAPIConnection()
        corpsheet = api.corp.CorporationSheet(userID=api_key.api_id, vCode=api_key.vcode, corporationID=self.corp_id)

        import evelogo
        evelogo.resourcePath = os.path.join(settings.PACKAGE_ROOT, "site_media/static/corplogos/")

        logo = evelogo.CorporationLogo(corpsheet.logo)
        logo.save(os.path.join(settings.PACKAGE_ROOT, "site_media/static/logos/%i.png" % (self.corp_id,) ))
        small = Image.open(os.path.join(settings.PACKAGE_ROOT, "site_media/static/logos/%i.png" % (self.corp_id,) ))
        tnsize = 32, 32
        small.thumbnail(tnsize)
        small.save(os.path.join(settings.PACKAGE_ROOT, "site_media/static/logos/%i.thumb.png" % (self.corp_id,) ))

        # TODO: Refactor this and above to be DRY
        self.ticker = corpsheet.ticker
        self.save()
    
    def get_logo_url(self, thumb=True):
        filename = "%i.png" % self.corp_id
        if thumb:
            filename = "%i.thumb.png" % self.corp_id
        return settings.STATIC_URL + "logos/%s" % filename

    def __unicode__(self):
        return u"%s" % (self.name,)

    def __str__(self):
        return str(self.__unicode__(),)

    def has_member(self, user):
        try:
            profile = user.get_profile()
        except:
            return False

        characters = profile.all_characters.all()
        for character in characters:
            if self == character.corp:
                return True

        return False

class Character(models.Model):
    account = models.ForeignKey(Account, related_name='all_characters')
    api_key = models.ForeignKey(APIKey, related_name='characters')
    character_id = models.IntegerField(primary_key=True, unique=True)
    corp = models.ForeignKey(Corporation)
    character_name = models.CharField(max_length=128, help_text="Character name")

    def __unicode__(self):
        return self.character_name

    def __str__(self):
        return str(self.character_name)
    
    def get_corp_name(self):
        return self.corp.name

    @classmethod
    def update_from_api(cls, apikey):
        api = eveapi.EVEAPIConnection()
        api_auth = api.auth(keyID=apikey.api_id, vCode=apikey.vcode)
        charlist = []
        try:
            retchars = api_auth.account.Characters()
        except:
            return []
        
        for retchar in retchars.characters:
            retchar_id = retchar.characterID
            retcorp_id = retchar.corporationID
            retcorp_name = retchar.corporationName

            try:
                corp = Corporation.objects.get(pk=retcorp_id)
            except:
                corp = Corporation(corp_id=retcorp_id, name=retcorp_name)
                corp.generate_logo(apikey)
                corp.save()

            character = cls(account=apikey.account,api_key=apikey,character_id=retchar_id,corp=corp,character_name=retchar.name)
            character.save()
            char_details = api_auth.eve.CharacterInfo(characterID=character.character_id)
            
            try:
                cs = CharacterSheet.objects.get(pk=character)
            except:
                if not hasattr(char_details, 'allianceID'):
                    alliance_id = None
                else:
                    alliance_id = char_details.allianceID
                    cs = CharacterSheet(character=character, corp=character.corp, alliance_id = alliance_id, sec_status = char_details.securityStatus)
                    cs.last_retrieved = timezone.now()
                    cs.save()
            charlist.append(character)
        
        return charlist

    def __unicode__(self):
        return u'%s' % (self.character_name,)

class CharacterSheet(models.Model):
    character = models.OneToOneField(Character, primary_key=True, unique=True, related_name='sheet')
    corp = models.ForeignKey(Corporation)
    alliance_id = models.IntegerField(blank=False, null=True)
    sec_status = models.IntegerField(blank=False, null=False)
    last_retrieved = models.DateTimeField(blank=False, null=True)
    
    def __unicode__(self):
        return self.character.character_name
    
    def __str__(self):
        return str(self.character.character_name)

class DefaultCharacter(models.Model):
    account = models.OneToOneField(Account, related_name='default_character')
    character = models.OneToOneField(Character, primary_key=True, related_name='default_for')

    class Meta:
        unique_together = ('account', 'character')

class Alliance(models.Model):
    alliance_id = models.IntegerField(primary_key=True)
    alliance_name = models.CharField(max_length=128)
    executor = models.ForeignKey(Corporation, related_name='executor_of')

    def has_member(self, user):
        alliance_profile = self.mgmt_profile
        corp_profiles = alliance_profile.member_corp_profiles
        for profile in corp_profiles.all():
            if profile.corporation.has_member(user):
                return True

        return False

    def __str__(self):
        return "<Alliance: %s>" % (self.alliance_name,)

@receiver(post_save, sender=DefaultCharacter)
def update_jid(sender, instance, created, **kwargs):
    domain = getattr(settings, 'EVE_DEFAULT_JABBER_DOMAIN', u'talkinlocal.org')
    if created:
        newjid = UserJID(instance.account.user, unicode(slugify(instance.character.character_name)), domain)
	newjid.save()
        return newjid
    
    currentjid = UserJID.objects.get(user=instance.account.user)

    # Check if anything's changed.
    if currentjid.node != unicode(slugify(instance.character.character_name)):
        currentjid.node = unicode(slugify(instance.character.character_name))
    # Ditto ; enforce configuration!
    if currentjid.domain != unicode(domain):
        currentjid.domain = unicode(domain)
    # Just in case
    currentjid.save()
    return currentjid

from account.fields import TimeZoneField
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^account\.fields\.TimeZoneField"],)
