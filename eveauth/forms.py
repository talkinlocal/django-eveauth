from django import forms
from .models import APIKey

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        exclude = ('account','date_added')
