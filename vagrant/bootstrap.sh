#!/bin/bash

apt-get update
apt-get install -y build-essential python-dev python-pip git python-virtualenv python-psycopg2 postgresql postgresql-server-dev-all sqlite3 screen libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

su -c 'bash /vagrant/vagrant/setup_virtualenv.sh' vagrant

echo '. /vagrant/vagrant/vagrant_env/bin/activate' >> /home/vagrant/.bashrc