from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
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

from models import APIKey
from forms import APIKeyForm

class APIKeyListView(BSListView):
    model = APIKey

    def _get_create_url(self):
        return reverse('apikey_add') 

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
        context = super(APIKeyListView, self).get_context_data(**kwargs)

        model_meta = self.model._meta

        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['add_object_url'] = self._get_create_url()

        return context

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
