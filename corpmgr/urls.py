from django.conf.urls.defaults import *
from django.conf import settings
from corpmgr.models import CorporationApplication
from corpmgr.views import CorpApplicationView, MyCorpApplicationsView, CorpApplicationDeleteView
from django.views.generic.base import TemplateView

from bootstrap.urls import bootstrap_delete

urlpatterns = patterns('corpmgr.views',
        url(r'^apply/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply'),
        url(r'^apply/(?P<cpid>)/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply_to'),
        url(r'^apply/success/$', TemplateView.as_view(template_name='corpmgr/app_success.html'), name='corpmgr_success'),
        #url(r'^apply/corporate/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
        #url(r'^apply/corporate/(?P<cpid>)/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
        url(r'^applications/$', MyCorpApplicationsView.as_view(), name='corpmgr_my_corp_app'),
        bootstrap_delete('^applications/(?P<pk>\d+)/delete/$', 'corp_application_delete', view=CorpApplicationDeleteView.as_view(), model=CorporationApplication),
)
