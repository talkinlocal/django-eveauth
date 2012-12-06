from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from datetime import datetime

from django.views.generic.base import RedirectView, View, TemplateResponseMixin
from django.views.generic.edit import FormView
from eveauth.views import OwnerListView

from bootstrap.views import (
                            CreateView as BSCreateView,
                            UpdateView as BSUpdateView,
                            ListView as BSListView,
                            DeleteView as BSDeleteView,
                            )

from account.utils import default_redirect, user_display

from django.template import RequestContext

from models import *
from forms import *

import os

class BaseRecommendationView(TemplateResponseMixin, View):
    model = Recommendation
    template_name = None
    application_model = None

    def get(self, request):
        user = request.user
        profile = user.get_profile()

        charlist = Character.objects.select_related().filter(account=profile)

        corplist = set([char.corp for char in charlist])

        applications = self.appliction_model.objects.filter(corporation__in=corplist).all()
        context = self.get_context_data()
        context = dict(content.items() + {'applications': applications}.items())

        rc = RequestContext(request, context)
        return self.render_to_response(rc)

class CorpRecommendationView(BaseRecommendationView):
    template_name = "corpmgr/member_recommendation.html"
    application_model = CorporationApplication

class AllianceRecommendationView(BaseRecommendationView):
    template_name = "corpmgr/corp_recommendation.html"
    application_model = AllianceApplication

class BaseApplicationView(FormView):
    def get_success_url(self):
        return reverse('corpmgr_my_corp_app')

class CorpApplicationView(BaseApplicationView):
    model = CorporationApplication
    form_class = CorpApplicationForm
    template_name = "corpmgr/member_application.html"
    
    def form_valid(self, form):
        u = self.request.user
        if u.is_authenticated():
            profile = u.get_profile()
            
            corp_app = form.save(commit=False)
            corp_app.created_by = profile
            corp_app.save()
            self.object = corp_app
            messages.success(self.request, 'Applied as %s to %s.' % (
                                                corp_app.character,
                                                corp_app.corporation_profile,
                                                ))
            return super(CorpApplicationView, self).form_valid(form)

        raise HttpResposeForbidden

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = {}
        context['corp_managed'] = True
        context['corporation_profiles'] = CorporationProfile.objects.all()
        context.update(**kwargs)

        return super(CorpApplicationView, self).get_context_data(**context)

    def form_invalid(self, form):
        messages.error(self.request, "Either your API Key does not meet the corporate minimum requirements, or your CEO key does not have the necessary information.")
        return self.render_to_response(self.get_context_data(form=form))


class AllianceApplicationView(BaseApplicationView):
    model = AllianceApplication
    template_name = "corpmgr/corp_application.html"

class CreatedByView(OwnerListView):

    def _get_create_url(self):
        return '/'

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            try:
                queryset = self.model._default_manager.filter(created_by=self.request.user.get_profile())
            except AttributeError:
                queryset=[]
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                    % self.__class__.__name__)

        return queryset

class MyCorpApplicationsView(CreatedByView):
    model = CorporationApplication
    template_name = "corpmgr/my_corp_apps.html"

class CorpApplicationDeleteView(BSDeleteView):
    model = CorporationApplication

    def get_success_url(self):
        return reverse('corpmgr_my_corp_app')
