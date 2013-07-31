from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.views import SignupView

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^auth/", include('eveauth.urls')),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^reddit/', include("vreddit.urls")), 
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
    url(r"^oauth/", include('oauth_provider.urls')),
    url(r"^forum/", include('forum.urls')),
    url(r"^corps/", include('corpmgr.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
