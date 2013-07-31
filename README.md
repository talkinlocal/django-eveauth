django-eveauth
====================

An EVE Online corp and access management application based on pinax-project-account

Example usage
=============

You will need to download http://dl.eve-files.com/media/corp/Entity/corplogos.7z and
have it uncompressed to use below

    $ git clone git@bitbucket.org:tsal/django-eveauth.git django-eveauth
    $ cd django-eveauth
    $ virtualenv eveauth_env
    $ source eveauth_env/bin/activate
    (eveauth_env)$ pip install -r requirements.txt
    (eveauth_env)$ python manage.py syncdb
    (eveauth_env)$ python manage.py migrate --all
    (eveauth_env)$ ln -s /path/to/corplogos static/corplogos
    (eveauth_env)$ python manage.py collectstatic --link
    (eveauth_env)$ mkdir -p site_media/media/logos/
    (eveauth_env)$ python manage.py runserver

Hit http://127.0.0.1:8000 to view the site!

What's included
===============

 * User profiles which are hooked up to the sign up process
 * API Key Management
 * Basic Corp Management
 * EVE-aware(ish) Forums

Common Issues
===============

The latest versions of ubuntu and debian have issues with PIL not including
zlib support.  Please look up instructions on how to get PIL and zlib working
in your environment. Likely the following links are missing:

    ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
    ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

Vagrant Development
===============

A simple Vagrantfile and bootstrap.sh have been added to the repository to allow for
quick provisioning of a development VM. After execution it should leave the vm such that
you can simply run

    $ vagrant ssh
    $ cd /vagrant
    $ python manage.py runserver 0.0.0.0:8000
