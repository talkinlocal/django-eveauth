from django import template
from django.template.defaultfilters import stringfilter
import string

register = template.Library()

@register.filter(name='jabberfy', is_safe=True)
@stringfilter
def make_jabber_username(username):
    username_stripped = ''.join((c for c in username if c in string.ascii_letters))
    username_stripped = username_stripped.lower()
    return username_stripped

