from django.contrib import admin

from models import RedditAccount, RedditConfirmation

class RedditAccountAdmin(admin.ModelAdmin):
    pass

class RedditConfirmationAdmin(admin.ModelAdmin):
    pass

admin.site.register(RedditAccount, RedditAccountAdmin)
admin.site.register(RedditConfirmation, RedditConfirmationAdmin)
