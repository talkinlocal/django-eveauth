from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from bootstrap.urls import bootstrap_list, bootstrap_create, bootstrap_update, bootstrap_delete
from forms import APIKeyForm
from models import APIKey
from views import *

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.views import SignupView
urlpatterns = patterns('',
        bootstrap_list(r'^$', 'apikey_list', model=APIKey, view=APIKeyListView.as_view()),
        bootstrap_create(r'^add/$', 'apikey_add', view=APIKeyCreateView.as_view(), form=APIKeyForm),
        bootstrap_update(r'^(?P<pk>\d+)/update/$', 'apikey_update', view=APIKeyUpdateView.as_view(), form=APIKeyForm),
        bootstrap_delete(r'^(?P<pk>\d+)/delete/$', 'apikey_delete', view=APIKeyDeleteView.as_view(), model=APIKey),
)

urlpatterns += patterns('',
        url(r'^characters/$', CharacterListView.as_view(), name="character_list"),
        url(r'^characters/update/$', CharacterUpdateView.as_view(), name="character_update"),
        url(r"^characters/default/$", DefaultCharacterView.as_view(), name="default_character"),
)
