from django.contrib import admin
from models import APIKey, Character, CharacterSheet, Corporation, Alliance

class APIKeyAdmin(admin.ModelAdmin):
    list_display = (
            'account',
            'get_formatted_characters',
            'api_id',
            'date_added',
            )

class CharacterAdmin(admin.ModelAdmin):
    search_fields=['character_name','corp__name','corp__ticker']
    list_display = (
            'character_name',
            'corp'
            )
    list_select_related = True

class CharacterSheetAdmin(admin.ModelAdmin):
    pass

class CorporationAdmin(admin.ModelAdmin):
    pass
    
class AllianceAdmin(admin.ModelAdmin):
    pass

admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterSheet, CharacterSheetAdmin)
admin.site.register(Corporation, CorporationAdmin)
admin.site.register(Alliance, AllianceAdmin)
