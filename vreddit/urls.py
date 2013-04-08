from django.conf.urls import patterns, include, url

from models import *
from forms import *
from views import *

urlpatterns = patterns("vreddit.views",

        url(r'^account/$', RedditVerifyView.as_view(), name="reddit_confirmation"),
        url(r'^authret/$', RedditReturnView.as_view(), name="reddit-return"),
)
