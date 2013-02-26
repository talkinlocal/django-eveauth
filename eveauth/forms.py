from django import forms
from models import APIKey, Character, Account, DefaultCharacter
from account.forms import SettingsForm
import eveapi

class AuthSettingsForm(SettingsForm):
    class Meta:
        model = Account

    def __init__(self, user, *args, **kwargs):
        super(AuthSettingsForm, self).__init__(*args, **kwargs)

        self.fields['default_character_id'] = forms.ModelChoiceField(queryset=Character.objects.filter(api_key__in=user.get_profile().apikeys.all()))

class DefaultCharacterForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(DefaultCharacterForm, self).__init__(*args, **kwargs)

        self.fields['character'].queryset = Character.objects.filter(account=user.get_profile())

        profile = user.get_profile()
        if hasattr(profile, 'default_character'):
            if user.get_profile().default_character is not None:
                self.initial['character'] = user.get_profile().default_character

    class Meta:
        model = DefaultCharacter
        exclude = ('account',)

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        exclude = ('account','date_added')

    def clean(self):
        cleaned_data = super(APIKeyForm, self).clean()

        api_id = cleaned_data.get("api_id")
        vcode = cleaned_data.get("vcode")

        api = eveapi.EVEAPIConnection()
        eve_auth = api.auth(keyID=api_id, vCode=vcode)

        try:
            keyinfo = eve_auth.account.APIKeyInfo()
        except:
            raise forms.ValidationError("Invalid API key.")

        access_mask = keyinfo.key.accessMask
        key_type = keyinfo.key.type
        is_mask = False
        acceptable_masks = []

        from django.conf import settings
        
        if "corpmgr" in settings.INSTALLED_APPS:
            from corpmgr.models import CorporationProfile
            if settings.EVE_CORP_MIN_MASK:
                acceptable_masks.append(settings.EVE_CORP_MIN_MASK)
            corp_profiles = CorporationProfile.objects.all()
            if corp_profiles.exists():
                for corp in corp_profiles:
                    acceptable_masks.append(corp.api_mask)

        if len(acceptable_masks) is 0:
            acceptable_masks.append(8)

        for mask in acceptable_masks:
            if (access_mask is mask) or ((access_mask & mask) == mask):
                is_mask = True

        if key_type == 'Account':
            if is_mask:
                return cleaned_data
        elif key_type == 'Corporation':
            return cleaned_data
        else:
            raise forms.ValidationError("No matching key masks or types.")

        # Fall through
        raise forms.ValidationError("No matching key masks or types.")
