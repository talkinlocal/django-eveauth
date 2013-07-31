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

class RedditConfirmationView(OwnerDetailsView):
    model = RedditAccount
    form_class = RedditAccountForm
    template_name = "vreddit/confirmation.html"

    def form_valid(self, form):
        u = self.request.user
        if u.is_authenticated():
            reddit_account = form.save(commit=False)
            reddit_account.account = u.get_profile()
            # Force it to create one
            reddit_account.save()
            confirmation = reddit_account.get_confirmation()
            confirmation.sent = timezone.now()
            confirmation.save()
            self.object = reddit_account

            return super(RedditConfirmationView, self).form_valid(form)

        raise HttpResponseForbidden

    def form_invalid(self, form):
        messages.error(self.request, mark_safe("Your reddit account is invalid.  Go away, nerd."))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('reddit_confirmation')

    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = request.user
        if not user.is_authenticated():
            messages.error(self.request, "You're not logged in.  You can't do that if you don't have an account and/or aren't logged in.  Pretty silly if you ask me.")
            return redirect("/account/login")

        account = user.get_profile()

        try:
            reddit_account = RedditAccount.objects.get(account=account)
        except:
            reddit_account = None

        if reddit_account:
            if reddit_account.verified:
                messages.error(self.request, "You're already verified, you can't be verified again.  Pretty silly if you ask me.")
                return redirect("/")

            confirmation = reddit_account.get_confirmation(create=False)

            context = self.get_context_data(form=form)

            if confirmation:
                if confirmation.sent and confirmation.key_expired():
                    messages.error("You apparently had an expired request and it has been deleted.  Please try again.")
                    confirmation.delete()
                    account.reddit_account.delete()
                    rc = RequestContext(request, context)
                    return self.render_to_response(rc)

                has_confirmation = True
            else:
                has_confirmation = False

            add_context = {
                        'has_confirmation': has_confirmation,
                        'confirmation': confirmation,
                        'reddit_account': reddit_account,
                        'reddit_subject': settings.REDDIT_AUTH_SUBJECT,
                        'site_reddit_user': settings.REDDIT_USER,
                        }
            context = dict(context.items() + add_context.items())
            rc = RequestContext(request, context)

            return self.render_to_response(rc)

        else:
            context = self.get_context_data(form=form)
            rc = RequestContext(request, context)

            return self.render_to_response(rc)

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
