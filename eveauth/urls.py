from django.conf.urls import patterns, include, url
from bootstrap.urls import bootstrap_list, bootstrap_update, bootstrap_delete, bootstrap_patterns, bootstrap_create

from .models import APIKey
from .forms import APIKeyForm
from .views import APIKeyCreateView, APIKeyUpdateView, APIKeyListView

# urlpatterns = patterns('eveauth.views',
        # bootstrap_list(r'^$', 'auth-index', model=APIKey),
# )

# urlpatterns = patterns('eveauth.views',
#        bootstrap_create('^add/$', 'apikey_form', view=APIKeyCreateView.as_view(), form=APIKeyForm),
#        bootstrap_list('^$', 'apikey_list', view=APIKeyListView.as_view(), model=APIKey),
#        bootstrap_update('^(?P<pk>\d+)/$', 'apikey_update', view=APIKeyUpdateView.as_view(), form=APIKeyForm),
#        bootstrap_delete('^(?P<pk>\d+)/delete/$', 'apikey_delete', model=APIKey),
#)


# urlpatterns = bootstrap_patterns(APIKeyForm)
