import logging
import os


# Forum Settings
FORUM_STANDALONE = False
FORUM_USE_REDIS = False
FORUM_POST_FORMATTER = 'forum.formatters.BBCodeFormatter'
FORUM_USE_DEFAULT_CHAR = True
BBCODE_AUTO_URLS = True

HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []

# Corp Manager
# Minimum api key mask (the bare minimum for access to SOME of our services)
EVE_CORP_MIN_MASK = 8388608

# ejabberd settings
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG = "/var/django/DEV/log/jabber_bridge.log"
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG = os.path.join(PROJECT_ROOT, "ejabber.log")
TUNNEL_EJABBERD_AUTH_GATEWAY_LOG_LEVEL = logging.DEBUG

# Mumble Options
TEST_MURMUR_LAB_DIR = "/var/django/DEV/murmur"
TEST_MURMUR_FILES_DIR = "/var/django/DEV/wheddit/murmur"
DEFAULT_CONN = 'Meta:tcp -h 127.0.0.1 -p 6502'
SLICE = '/usr/share/slice/Murmur.ice'
SLICEDIR = '/usr/share/slice'
MUMBLE_DJANGO_URL = '/'
MUMBLE_DJANGO_ROOT = '/var/django/DEV/wheddit'
