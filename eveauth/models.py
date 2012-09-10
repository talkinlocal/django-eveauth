from django.db import models
from account.models import Account
from datetime import datetime
import eveapi

class APIKey(models.Model):
    account = models.ForeignKey(Account, related_name='apikeys')
    api_id = models.IntegerField(primary_key=True, unique=True, help_text="The number ID of your API key")
    vcode = models.CharField(max_length=255, help_text="The verification code of your API key")
    date_added = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u"%s - %s (added %s)" % ( self.api_id, self.vcode, self.date_added) 

    def __str__(self):
        return str(self.__unicode__())


class Character(models.Model):
    account = models.ForeignKey(Account)
    api_key = models.ForeignKey(APIKey, related_name='characters')
    character_id = models.IntegerField(primary_key=True, unique=True)
    corp_id = models.IntegerField(blank=True, null=True)
    character_name = models.CharField(max_length=128, help_text="Character name")

    def __unicode__(self):
        return self.character_name

    def __str__(self):
        return str(self.character_name)
    
    @classmethod
    def update_from_api(cls, apikey):
        api = eveapi.EVEAPIConnection()
        api_auth = api.auth(keyID=apikey.api_id, vCode=apikey.vcode)
        charlist = []
        try:
            retchars = api_auth.account.Characters()
        except e:
            raise e
            
        
        for retchar in retchars.characters:
            retchar_id = retchar.characterID
            retcorp_id = retchar.corporationID
            character = cls(account=apikey.account,api_key=apikey,character_id=retchar_id,corp_id=retcorp_id,character_name=retchar.name)
            character.save()
            char_details = api_auth.eve.CharacterInfo(characterID=character.character_id)
            cstry = CharacterSheet.objects.filter(character=character)
            if not cstry:
                if not hasattr(char_details, 'allianceID'):
                    alliance_id = None
                else:
                    alliance_id = char_details.allianceID
                cs = CharacterSheet(character=character, corporation_id=char_details.corporationID, alliance_id = alliance_id, sec_status = char_details.securityStatus)
            else:
                cs = cstry
            cs.last_retrieved = datetime.now()
            cs.save()
            charlist.append(character)
        
        return charlist

class CharacterSheet(models.Model):
    character = models.OneToOneField(Character, unique=True, related_name='sheet')
    corporation_id = models.IntegerField(blank=False, null=False)
    alliance_id = models.IntegerField(blank=False, null=True)
    sec_status = models.IntegerField(blank=False, null=False)
    last_retrieved = models.DateTimeField(blank=False, null=True)
    
    def __unicode__(self):
        return self.character.character_name
    
    def __str__(self):
        return str(self.character.character_name)
