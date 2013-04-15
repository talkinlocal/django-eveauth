from django.db import models
from django.contrib.auth.models import User, AnonymousUser, Group
from django.contrib.sites.models import Site
from django.db.models.signals import post_save

from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

import eveapi, os, Image

class Domain(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % (self.name,)

class UserJID(models.Model):
    site_user = models.OneToOneField(User, related_name='jid', primary_key=True)
    node = models.CharField(max_length=256, null=False, blank=False)
    domain = models.ForeignKey(Domain, related_name='jids', null=False)

    class Meta:
        unique_together = ('node', 'domain')

    def asJID(self):
        return self.__unicode__()

    @classmethod
    def fromJID(cls, jid):
        try:
            node, domain = jid.split(u'@')
            domain = domain.split(u'/')[0]
            return cls.objects.get(node=node, domain=Domain.objects.get(name=u'%s' % (domain.lower(),)))
        except cls.DoesNotExist:
            # for re-raising later
            import sys
            exc_info = sys.exc_info()
            # check if there's a matching (ish) domain and user if configured to do so
            if hasattr(settings, 'EVE_DEFAULT_JABBER_DOMAIN'):
                # Just wanted to note, the below 4 lines make my head hurt, and here's why:
                # I should never need this code, but had I not implemented it, some day I'd 
                # run into an error redeploying this application and come across this weird,
                # f-d up error involving migrations or something and have no idea wtf to do
                # to fix it until 2 days later I realized I was missing the default domain 
                # in the database.
                # TODO: implement fixtures when I can be bothered to, eliminating this code.
                try:
                    domain = Domain.objects.get(name__iexact=domain)
                except Domain.DoesNotExist:
                    domain = Domain(u'%s' % (domain,))
                    domain.save() # TODO: hooks to create vhost in ejabberd w/ xmlrpc

                if domain.name == settings.EVE_DEFAULT_JABBER_DOMAIN:
                    # Just in case...
                    try:
                        user = User.objects.get(username__iexact=node)
                    except User.DoesNotExist:
                        # because they asked for a THIS dang it!
                        raise exc_info[0], exc_info[1], exc_info[2]
                    # Create one
                    return cls(node=user.username.lower(), domain=domain)

            else:
                raise 

    def __unicode__(self):
        return u'%s@%s' % (self.node, self.domain)

class SharedRosterGroup(models.Model):
    site_group = models.OneToOneField(Group, related_name='srg', primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    domain = models.ForeignKey(Domain)
    members = models.ManyToManyField(UserJID)

