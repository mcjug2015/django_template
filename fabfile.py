#!/usr/bin/env python
from fabric.api import env, local, sudo, require, run, put, settings, cd, lcd
import os
import sys
import time


env.prj_name = 'django_template'
env.path = '/opt/%(prj_name)s' % env


def local_box():
    env.instance = 'local_box'


def _ensure_virtualenv():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found. Make sure to activate virtualenv first\n\n")
        sys.exit(-1)
    env.virtualenv = os.environ["VIRTUAL_ENV"]


def copy_settings():
    require('instance')
    local('cp django_template/environments/%(instance)s/settings/%(instance)s.py django_template/settings.py' % env)


def install_prod_deps():
    _ensure_virtualenv()
    local('pip install -q -r %(path)s/dependencies/prod.txt' % env)
