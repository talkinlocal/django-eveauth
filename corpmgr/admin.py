from django.contrib import admin
from models import *

class CorpProfileAdmin(admin.ModelAdmin):
    list_display = (
            'corporation',
            'manager',
            'director_group',
            'reddit_required',
            )

admin.site.register(CorporationProfile, CorpProfileAdmin)
