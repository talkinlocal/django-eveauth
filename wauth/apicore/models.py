from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import eveapi

from userena.models import UserenaBaseProfile

class AuthProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name='user', related_name='my_profile')
    
class APIKey(models.Model):
    auth_id = models.ForeignKey(AuthProfile)
    api_id = models.IntegerField(primary_key=True, unique=True, help_text="The number ID of your API key")
    vcode = models.CharField(max_length=255, help_text="The verification code of your API key")
    
class Character(models.Model):
    auth_id = models.ForeignKey(AuthProfile)
    api_id = models.ForeignKey(APIKey)
    character_id = models.IntegerField(primary_key=True, unique=True)
    corp_id = models.IntegerField(blank=True, null=True)
    
    @classmethod
    def update_from_api(cls, apikey):
        api = eveapi.EVEAPIConnection()
        api_auth = api.auth(keyID=apikey.api_id, vCode=apikey.vcode)
        charlist = []
        try:
            retchars = api_auth.account.Characters()
        except:
            pass
        
        for retchar in retchars:
            retchar_id = retchar.characterID
            retcorp_id = retchar.corporationID
            character = cls(auth_id=apikey.auth_id,api_id=apikey.api_id,character_id=retchar_id,corp_id=retcorp_id)
            charlist.append(character)
        
        return charlist
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AuthProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
