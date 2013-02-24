from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from datetime import datetime

from django.views.generic.base import (RedirectView,
        View, TemplateResponseMixin)
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
from django.template.response import TemplateResponse

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

        applications = self.appliction_model.objects.filter(
                                    corporation__in=corplist).all()
        context = self.get_context_data()
        context = dict(content.items() + {
                                'applications': applications,
                            }.items())

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
        messages.error(self.request,
"""
Either your API Key does not meet the corporate minimum requirements,
or your CEO key does not have the necessary information.
""")
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
                queryset = self.model._default_manager.filter(
                        created_by=self.request.user.get_profile()
                        )
            except AttributeError:
                queryset=[]
        else:
            raise ImproperlyConfigured(
                    "'%s' must define 'queryset' or 'model'" % (
                            self.__class__.__name__,
                        )
                    )

        return queryset

class MyCorpApplicationsView(CreatedByView):
    model = CorporationApplication
    template_name = "corpmgr/my_corp_apps.html"

class CorpApplicationDeleteView(BSDeleteView):
    model = CorporationApplication

    def get_success_url(self):
        return reverse('corpmgr_my_corp_app')

class DirectorCorpView(TemplateResponseMixin, View):
    template_name = "corpmgr/director_corp_dashboard.html"
    statuses = {'new': (0,1), 'pending': 1, 'approved': 2 }
    
    def get(self, request, **kwargs):
        corp_id = kwargs.get('corpid', None)
        user = request.user

        if not user.is_authenticated():
            return redirect("/account/login")

        if corp_id is not None:
            try:
                corporation = Corporation.objects.get(corp_id=corp_id)
            except Corporation.DoesNotExist:
                return redirect("/corps/director/")

            profile = corporation.mgmt_profile
            
            if not profile.has_director(user):
                return redirect("/account/login/")

            status_code = getattr(kwargs, 'status', None)

            if status_code is None:
                status_code = 'new'

            status = self.statuses[status_code]

            pending_apps = profile.pending_applications(status)

            cdict = {'pending_apps': pending_apps,}

            rc = RequestContext(request, cdict)

            return self.render_to_response(rc)

class DirectorDashboardView(TemplateResponseMixin, View):
    template_name = "corpmgr/director_dashboard.html"

    def get(self, request, **kwargs):
        user = request.user
        director_of = []
        exec_director_of = []

        for corp in CorporationProfile.objects.all():
            if corp.has_director(user):
                director_of.append(corp)
            elif corp.manager is user:
                director_of.append(corp)

        for alliance in AllianceProfile.objects.all():
            if alliance.has_director(user):
                exec_director_of.append(alliance)
            elif alliance.manager is user:
                exec_director_of.append(alliance)

        pending_apps = 0

        for corp in director_of:
            pending_apps += len(corp.pending_applications())

        cdict = {
                "pending_applications": pending_apps,
                "director_of": director_of,
                "exec_director_of": exec_director_of,
                }

        rc = RequestContext(request, cdict)

        return self.render_to_response(rc)

class DirectorAppUpdate(TemplateResponseMixin, View):
    template_name = "corpmgr/director_corp_dashboard.html"

    def get(self, request, **kwargs):
        application = CorporationApplication.objects.get(pk=kwargs['appid'])
        corp_profile = application.corporation_profile
        corp_id = corp_profile.corporation.corp_id
        character = application.character
        status = kwargs['status']
        user = request.user

        if corp_profile.has_director(user):
            if status is 2:
                application.approve()
                application.approved_by = user.get_profile()
                application.save()
            if status is 1:
                application.pending()
                application.save()

            return redirect("/corps/director/%d/" % (corp_id,))

        return TemplateResponse(request, self.template_name, {'corpid': corp_id, 'status': 'new'})
