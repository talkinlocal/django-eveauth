from django.conf.urls.defaults import *
from django.conf import settings
from corpmgr.models import CorporationApplication
from django.contrib.auth.decorators import login_required
from corpmgr.views import *
from django.views.generic.base import TemplateView

from bootstrap.urls import bootstrap_delete

urlpatterns = patterns('corpmgr.views',
        url(r'^apply/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply'),
        url(r'^apply/(?P<cpid>)/$', CorpApplicationView.as_view(), name='corpmgr_corp_apply_to'),
        url(r'^apply/success/$', TemplateView.as_view(template_name='corpmgr/app_success.html'), name='corpmgr_success'),
        #url(r'^apply/corporate/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
        #url(r'^apply/corporate/(?P<cpid>)/$', AllianceApplicationView.as_view(), name='corpmgr_alliance_apply'),
        url(r'^applications/$', MyCorpApplicationsView.as_view(), name='corpmgr_my_corp_app'),
        url(r'^director/$', login_required(DirectorDashboardView.as_view()), name='director_dashboard'),
        url(r'^director/(?P<corpid>\d+)/$', login_required(DirectorCorpView.as_view()), name='director_corp_dashboard'),
        url(r'^director/(?P<corpid>\d+)/approved/$', login_required(DirectorCorpView.as_view()), {'status': 'approved'}, 'director_corp_dashboard_approved'),
        url(r'^director/(?P<corpid>\d+)/pending/$', login_required(DirectorCorpView.as_view()), {'status': 'pending'}, 'director_corp_dashboard_pending'),
        url(r'^director/approve/(?P<appid>\d+)/$', login_required(DirectorAppUpdate.as_view()), {'status': 2}),
        bootstrap_delete('^applications/(?P<pk>\d+)/delete/$', 'corp_application_delete', view=CorpApplicationDeleteView.as_view(), model=CorporationApplication),
)
