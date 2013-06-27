#!/bin/bash

virtualenv /vagrant/vagrant/vagrant_env

. /vagrant/vagrant/vagrant_env/bin/activate

pip install -r /vagrant/requirements.txt