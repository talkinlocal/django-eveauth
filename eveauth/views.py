from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#from django.views.generic.list import ListView

from datetime import datetime

from decorators import group_required, multigroup_required

from bootstrap.views import (
                            CreateView as BSCreateView,
                            UpdateView as BSUpdateView,
                            ListView as BSListView,
                            DeleteView as BSDeleteView,
                            )
from django.views.generic.base import RedirectView, View, TemplateResponseMixin
from django.views.generic.edit import FormView

from account.views import SettingsView
from account.views import SignupView as DefSignupView
from account.utils import default_redirect, user_display

from django.template import RequestContext

from eveauth.tasks import update_characters

from models import APIKey, Character, DefaultCharacter

if "corpmgr" in settings.INSTALLED_APPS:
    from corpmgr.models import CorporationProfile

from forms import APIKeyForm, DefaultCharacterForm
import os

class CharacterUpdateView(TemplateResponseMixin, View):
    model = Character
    template_name = "eveauth/character_list.html"

    def get(self, request):
        user = self.request.user

        #update_characters(user)
        update_characters.delay(user)

        allchars = []

        try:
            user.get_profile()
        except AttributeError:
            messages.error(self.request, mark_safe("You're not logged in, nerd."))
            context = self.get_context_data()
            context = dict(context.items() + {'object_list': []}.items())
            rc = RequestContext(request, context)
            return redirect("/account/login/")

        # for apikey in user.get_profile().apikeys.all():
            # allchars.append([char for char in apikey.characters.all()])

        context = self.get_context_data()
        #context = dict(context.items() + {'object_list': allchars}.items())

        rc = RequestContext(request, context)
        messages.success(self.request, "Backend API request submitted.  Normally this takes seconds to complete, but can take up to 2 hours under heavy load.")

        return redirect("/auth/characters/")
        #return self.render_to_response(rc)

    def get_context_data(self, **kwargs):
        model_meta = self.model._meta

        cdict = {}

        cdict['model_verbose_name'] = model_meta.verbose_name
        cdict['model_verbose_name_plural'] = model_meta.verbose_name_plural

        cdict['is_updating'] = True

        return cdict

class OwnerListView(BSListView):

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            try:
                queryset = self.model._default_manager.filter(account=self.request.user.get_profile())
            except AttributeError:
                queryset = []
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                        % self.__class__.__name__)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OwnerListView, self).get_context_data(**kwargs)

        model_meta = self.model._meta

        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['add_object_url'] = self._get_create_url()

        return context

class APIKeyListView(OwnerListView):
    model = APIKey

    def _get_create_url(self):
        return reverse('apikey_add') 


class CharacterListView(OwnerListView):
    model = Character
    template_name = "eveauth/character_list.html"

    def _get_create_url(self):
        return ''

class APIKeyDeleteView(BSDeleteView):
    model = APIKey
    template_name = "eveauth/apikey_delete.html"

    def get_success_url(self):
        return reverse('apikey_list')

#@group_required('Registered')
class APIKeyCreateView(BSCreateView):
    model = APIKey
    form_class = APIKeyForm
    template_name = "eveauth/apikey_add.html"

    def form_valid(self, form):
        u = self.request.user
        if u.is_authenticated():
            apikey = form.save(commit=False)
            apikey.account = u.get_profile()
            apikey.date_added = datetime.now()
            apikey.save()
            self.object = apikey
            try:
                from metron import activity

                activity.add(request, "mixpanel", "track", "API Added", {
                    "user": u.username,
                    })
            except:
                pass
            return super(APIKeyCreateView, self).form_valid(form)

        raise HttpResponseForbidden

    def form_invalid(self, form):
        from django.conf import settings

        error_message = """
Our minimum API key mask is '8'.  You can start with a predefined key 
<a href="https://support.eveonline.com/api/Key/CreatePredefined/%s">here</a>
Your key must contain all characters, not just one.
Please assure you meet these requirements.
"""
        if settings.EVE_CORP_MIN_MASK:
            messages.error(self.request, mark_safe( error_message % (
                settings.EVE_CORP_MIN_MASK
                )))
        else:
            messages.error(self.request, mark_safe( error_message % (8,)))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('apikey_list')

    def get_context_data(self, **kwargs):
        context = {}

        if "corpmgr" in settings.INSTALLED_APPS:
            context['corp_managed'] = True
            corp_profiles = CorporationProfile.objects.all()
            context['corporation_profiles'] = corp_profiles

            if settings.EVE_CORP_MIN_MASK:
                context['min_mask'] = settings.EVE_CORP_MIN_MASK

        context.update(kwargs)

        return super(APIKeyCreateView, self).get_context_data(**context)

class APIKeyUpdateView(BSUpdateView):
    model = APIKey
    form_class = APIKeyForm
    template_name = "eveauth/apikey_update.html"

    def form_valid(self, form):
        u = self.request.user
        if u.is_authenticated():
            apikey = form.save(commit=False)
            if (apikey.account is u.account) or u.is_superuser:
                apikey.save()
                self.object = apikey
                return super(APIKeyUpdateView, self).form_valid(form)

        raise HttpResponseForbidden

    def get_success_url(self):
        return reverse('apikey_list')

    def _get_delete_url(self):
        return reverse('apikey_delete', kwargs={'pk': self.object.api_id})


class DefaultCharacterView(FormView):
    form_class = DefaultCharacterForm
    model = DefaultCharacter
    template_name = "eveauth/default_character.html"

    def form_valid(self, form):
        u = self.request.user
        if u.is_authenticated():
            profile = u.get_profile()
            if hasattr(profile, 'default_character'):
                char = profile.default_character.character
                profile.default_character.delete()
                messages.info(self.request, 'Removed %s as default character' % (char,))
            defaultchar = form.save(commit=False)
            defaultchar.account = u.get_profile()
            defaultchar.save()
            self.object = defaultchar
            messages.success(self.request, 'Set %s as default character.' % (defaultchar.character,))
            return super(DefaultCharacterView, self).form_valid(form)

        raise HttpResponseForbidden

    def get_success_url(self):
        return reverse("default_character")

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())

