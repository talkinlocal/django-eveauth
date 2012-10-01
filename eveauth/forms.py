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
        except eveapi.AuthenticationError:
            raise forms.ValidationError("Invalid API key.")

        access_mask = keyinfo.key.accessMask
        key_type = keyinfo.key.type
        
        is_mask = (access_mask & 61746010) == 61746010
        is_type = key_type == u'Account'
        if not is_mask or not is_type:
            raise forms.ValidationError("API Key Invalid - you MUST use mask 61746010 and Account key types!")

        return cleaned_data
