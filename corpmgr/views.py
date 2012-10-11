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

from account.utils import default_redirect, user_display

from django.template import RequestContext

from models import *

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
