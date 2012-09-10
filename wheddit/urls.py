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

from .views import SignupView
from eveauth.views import APIKeyCreateView, APIKeyUpdateView, APIKeyListView

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
#    url(r'^auth/$', include('eveauth.urls', namespace="eveauth")),
)

#urlpatterns += bootstrap_patterns(APIKeyForm)

urlpatterns += patterns('',
        bootstrap_list(r'^auth/$', 'apikey_list', model=APIKey, view=APIKeyListView.as_view()),
        bootstrap_create(r'^auth/add/$', 'apikey_add', view=APIKeyCreateView.as_view(), form=APIKeyForm),
        #url(r"^auth/?P<pk\d+)/$", APIKeyDetailView.as_view(), name="apikey_details"),
        bootstrap_update(r'^auth/(?P<pk>\d+)/update/$', 'apikey_update', view=APIKeyUpdateView.as_view(), form=APIKeyForm),
        bootstrap_delete(r'^auth/(?P<pk>\d+)/delete/$', 'apikey_delete', view=APIKeyDeleteView.as_view(), model=APIKey),
)

#urlpatterns += patterns("",
        #url(r"^auth/", include((bootstrap_patterns(APIKeyForm), 'eveauth', 'eveauth'))),
#)




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
