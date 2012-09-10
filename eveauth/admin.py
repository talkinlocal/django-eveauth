from django.contrib import admin
from models import APIKey, Character, CharacterSheet

class APIKeyAdmin(admin.ModelAdmin):
    pass

class CharacterAdmin(admin.ModelAdmin):
    pass

class CharacterSheetAdmin(admin.ModelAdmin):
    pass

admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterSheet, CharacterSheetAdmin)
