django-eveauth
====================

an EVE Online corp and access managment application based on pinax-project-account

Example usage
=============

You will need to download http://dl.eve-files.com/media/corp/Entity/corplogos.7z and
install the corplogos folder below.

    $ git clone git@bitbucket.org:tsal/django-eveauth.git mysite
    $ virtualenv mysite
    $ cd mysite
    $ source mysite/bin/activate
    (mysite)$ pip install -r requirements.txt
    (mysite)$ python manage.py syncdb
    (mysite)$ python manage.py migrate
    (mysite)$ cp -rp /path/to/corplogos eveauth/static/
    (mysite)$ python manage.py collectstatic
    (mysite)$ mkdir -p path/to/site_media/static/logos/
    (mysite)$ python manage.py runserver

Hit http://127.0.0.1:8000 to view the site!

What's included
===============

 * user profiles which are hooked up to the sign up process
 * API Key Management
 * Basic Corp Management
 * EVE-aware(ish) Forums


Common Issues
===============

The latest versions of ubuntu and debian have issues with PIL not including
zlib support.  Please look up instructions on how to get PIL and zlib working
in your environment.
