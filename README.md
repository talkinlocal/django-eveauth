django-eveauth
====================

an EVE Online corp and access managment application based on pinax-project-account

Example usage
=============

    $ virtualenv mysite
    $ source mysite/bin/activate
    (mysite)$ pip install Django==1.4.1
    (mysite)$ git clone git@bitbucket.org:tsal/django-eveauth.git
    (mysite)$ cd mysite
    (mysite)$ pip install -r requirements.txt
    (mysite)$ python manage.py syncdb
    (mysite)$ python manage.py runserver

Hit http://127.0.0.1:8000 to view the site!

What's included
===============

 * user profiles which are hooked up to the sign up process
 * API Key Management
 * Basic Corp Management
 * EVE-aware(ish) Forums
