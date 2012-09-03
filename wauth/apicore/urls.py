from django.conf.urls import patterns, include, url

urlpatterns = patterns('apicore.views',
        url(r'^$', 'index'),
)
