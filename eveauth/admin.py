from django.contrib import admin
from models import APIKey, Character, CharacterSheet, Corporation

class APIKeyAdmin(admin.ModelAdmin):
    list_display = (
            'account',
            'get_formatted_characters',
            'api_id',
            'date_added',
            )

class CharacterAdmin(admin.ModelAdmin):
    pass

class CharacterSheetAdmin(admin.ModelAdmin):
    pass

class CorporationAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterSheet, CharacterSheetAdmin)
admin.site.register(Corporation, CorporationAdmin)
