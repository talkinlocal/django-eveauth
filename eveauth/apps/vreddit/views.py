from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

from datetime import datetime

from django.views.generic.base import RedirectView, View, TemplateResponseMixin
from django.views.generic.edit import FormView

from account.utils import default_redirect, user_display

from django.template import RequestContext

from eve_auth.tasks import update_characters

from models import RedditAccount, RedditConfirmation
from forms import RedditAccountForm

import os

from hashlib import sha1
import praw

class OwnerDetailsView(FormView):
    pass

def generate_state_key(pre_code, secret, username):
    pre_state = "%s%s" % (secret,username)
    key = sha1(pre_state).hexdigest()
    state_key = "%s%s" % (pre_code,key)
    return 

def get_reddit_client(redirect_uri):
    r  = praw.Reddit(
            'Talk In Local - eve_auth.org reddit verification v1.0'
            )

    r.set_oauth_app_info(
            client_id = settings.REDDIT_APP_ID,
            client_secret = settings.REDDIT_APP_SECRET,
            redirect_uri=redirect_uri)

    return r

class RedditVerifyView(View):
    template_name = "vreddit/verify.html"
    def get(self, request, *args, **kwargs):
        auth_url = 'https://ssl.reddit.com/api/v1/' # TODO: move this to settings.py
        try:
            redditacct = RedditAccount.objects.get(account=request.user.get_profile())
            if redditacct.access_token:
                messages.error(self.request, mark_safe("Your account is already linked to: %s" % (redditacct.reddit_login)))
                return redirect('/')
            else:
                messages.warning(self.request, mark_safe("Old reddit verification found, processed new verification."))
        except RedditAccount.DoesNotExist:
            pass

        redirect_uri = request.build_absolute_uri(reverse('reddit-return'))
        # This should always be the same.
        state_key = "TILVerify"
        # TODO: Make configurable
        r = get_reddit_client(redirect_uri)
        url = r.get_authorize_url(state_key, 'identity', False)

        return redirect(url)

class RedditReturnView(View,TemplateResponseMixin):
    template_name = "vreddit/oauth_return.html"
    
    def get(self, request, *args, **kwargs):
        incoming_code = request.GET.get('code', None)
        incoming_state = request.GET.get('state', None)
        if incoming_code and incoming_state:
            state_key = "TILVerify"
            if state_key == incoming_state:
                r = get_reddit_client(request.build_absolute_uri(reverse('reddit-return')))
                access_information = r.get_access_information(incoming_code)
                authenticated_user = r.get_me()

                try:
                    reddit = RedditAccount.objects.get(reddit_login=authenticated_user.name)
                    if reddit.access_token:
                        messages.error(self.request, mark_safe("An account is already linked to: %s" % (reddit.reddit_login)))
                        redirect('/')
                    if reddit.account == request.user.get_profile():
                        reddit.access_token = access_information['access_token']
                        messages.success(self.request, mark_safe("Converted old verification for reddit account: %s" % (authenticated_user.name,)))
                    else:
                        messages.error(self.request, mark_safe("Your account is already linked to: %s and does not match this link request: %s" % (reddit.reddit_login, authenticated_user.name)))
                        redirect('/')

                except RedditAccount.DoesNotExist:
                    # Good
                    reddit = RedditAccount(
                            account = request.user.get_profile(),
                            reddit_login = authenticated_user.name,
                            verified = True,
                            access_token = access_information['access_token'],
                            refresh_token = access_information['refresh_token'],
                            )

                finally:
                    reddit.save()

        else:
            messages.error(request, mark_safe("unknown error: %s" % (request.GET,)))

        return redirect('/')
