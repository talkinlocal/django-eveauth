from django.conf.urls.defaults import *
from django.conf import settings
from corpmgr.views import CorpApplicationView

urlpatterns = patterns('corpmgr.views',
        url(r'^apply/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply'),
        url(r'^apply/(?P<cpid>)/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply_to'),
        #url(r'^apply/corporate/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
        #url(r'^apply/corporate/(?P<cpid>)/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
)
