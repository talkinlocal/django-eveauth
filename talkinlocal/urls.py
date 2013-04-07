from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from bootstrap.urls import bootstrap_list, bootstrap_create, bootstrap_update, bootstrap_delete
from eveauth.forms import APIKeyForm
from eveauth.models import APIKey
from eveauth.views import *

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.views import SignupView
from eveauth.views import *

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^reddit/', include("vreddit.urls")), 
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
    url(r"^oauth/", include('oauth_provider.urls')),
    url(r"^forum/", include('forum.urls')),
    url(r"^corps/", include('corpmgr.urls')),
)

#urlpatterns += bootstrap_patterns(APIKeyForm)

urlpatterns += patterns('',
        bootstrap_list(r'^auth/$', 'apikey_list', model=APIKey, view=APIKeyListView.as_view()),
        bootstrap_create(r'^auth/add/$', 'apikey_add', view=APIKeyCreateView.as_view(), form=APIKeyForm),
        #url(r"^auth/?P<pk\d+)/$", APIKeyDetailView.as_view(), name="apikey_details"),
        bootstrap_update(r'^auth/(?P<pk>\d+)/update/$', 'apikey_update', view=APIKeyUpdateView.as_view(), form=APIKeyForm),
        bootstrap_delete(r'^auth/(?P<pk>\d+)/delete/$', 'apikey_delete', view=APIKeyDeleteView.as_view(), model=APIKey),
)

urlpatterns += patterns('',
        url(r'^auth/characters/$', CharacterListView.as_view(), name="character_list"),
        url(r'^auth/characters/update/$', CharacterUpdateView.as_view(), name="character_update"),
        url(r"^auth/characters/default/$", DefaultCharacterView.as_view(), name="default_character"),
)
#urlpatterns += patterns("",
        #url(r"^auth/", include((bootstrap_patterns(APIKeyForm), 'eveauth', 'eveauth'))),
#)




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
