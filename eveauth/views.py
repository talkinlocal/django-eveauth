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

from account.views import SettingsView

from django.template import RequestContext

from eveauth.tasks import update_characters

from models import APIKey, Character
from forms import APIKeyForm, AuthSettingsForm
import os

class CharacterUpdateView(TemplateResponseMixin, View):
    model = Character
    template_name = "eveauth/character_list.html"

    def get(self, request):
        user = self.request.user

        update_characters(user)
        #update_characters.delay(user)

        messages.success(self.request, "Backend API request submitted.  Normally this takes seconds to complete, but can take up to 2 hours under heavy load.")

        allchars = []

        for apikey in user.get_profile().apikeys.all():
            allchars.append([char for char in apikey.characters.all()])

        context = self.get_context_data()
        context = dict(context.items() + {'object_list': allchars}.items())

        rc = RequestContext(request, context)
        return self.render_to_response(rc)

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
            queryset = self.model._default_manager.filter(account=self.request.user.get_profile())
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'mode;'"
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

    def _get_create_url(self):
        return ''

class APIKeyDeleteView(BSDeleteView):
    model = APIKey

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
            apikey.account = u.account
            apikey.date_added = datetime.now()
            apikey.save()
            self.object = apikey
            return super(APIKeyCreateView, self).form_valid(form)

        raise HttpResponseForbidden

    def form_invalid(self, form):
        import django.contrib.messages
        messages.error(self.request, mark_safe("Your API key is either invalid or is not made to our requirements.  Please use <a href='https://support.eveonline.com/api/key/CreatePredefined/61746010' target='_blank'>this pre-made key template</a>."))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('apikey_list')

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

        raise HttpReponseForbidden

    def get_success_url(self):
        return reverse('apikey_list')

    def _get_delete_url(self):
        return reverse('apikey_delete', kwargs={'pk': self.object.api_id})


class AuthSettingsView(SettingsView):
    template_name = "eveauth/settings.html"
    form_class = AuthSettingsForm
    messages = {
            "settings_updated": {
                "level": messages.SUCCESS,
                "text": _("Auth settings updated.")
                },

            "no_api_keys": {
                "level": messages.WARNING,
                "text": _("No API Keys defined, please add an API Key.")
                },

            "no_characters": {
                "level": messages.WARNING,
                "text": _("No characters found. Please 'Update Characters'.")
                },
                
            }

    def get_form(self, form_class):
        """
        Returns an instance of the form with passed user information.
        """
        return form_class(self.request.user, **self.get_form_kwargs())

    def get_initial(self):
        if not self.request.user.get_profile().apikeys.all():
            if self.messages.get("no_api_keys"):
                messages.add_message(
                        self.request,
                        self.messages["no_api_keys"]["level"],
                        self.messages["no_api_keys"]["text"]
                )
        else:
            no_chars = False
            for apikey in self.request.user.get_profile().apikeys.all():
                if not apikey.characters.all():
                    no_chars = True

            if no_chars:
                if self.messages.get("no_characters"):
                    messages.add_message(
                            self.request,
                            self.messages["no_characters"]["level"],
                            self.messages["no_characters"]["text"]
                    )
        initial = super(AuthSettingsView, self).get_initial()
        if self.request.user.get_profile().default_character_id:
            initial["default_character_id"] = self.request.user.get_profile().default_character_id

