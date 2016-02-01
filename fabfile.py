#!/usr/bin/env python
from fabric.api import env, local, sudo, require, run, put, settings, cd, lcd
import os
import sys


env.prj_name = 'django_template'
env.path = '/opt/%(prj_name)s' % env


def one_time_node_install():
    ''' installs node into currently sourced virtualenv, no existence checks done. '''
    _ensure_virtualenv()
    with lcd('/tmp'):
        local('curl http://nodejs.org/dist/node-latest.tar.gz | tar xvz')
        with lcd('node-v*'):
            local('./configure --prefix=$VIRTUAL_ENV')
            local('make install')
    local('rm -rf /tmp/node-v*')


def local_box():
    env.instance = 'local_box'


def unit_test():
    env.instance = 'unit_test'


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


def install_all_deps():
    _ensure_virtualenv()
    install_prod_deps()
    local('pip install -q -r %(path)s/dependencies/dev.txt' % env)


def pylint():
    _ensure_virtualenv()
    local('pylint --rcfile=conf/pylintrc.txt template_app | tee reports/template_app_pylint.txt; test ${PIPESTATUS[0]} -eq 0')
    local('pylint --rcfile=conf/pylintrc.txt django_template | tee reports/django_template_pylint.txt; test ${PIPESTATUS[0]} -eq 0')


def pep8():
    _ensure_virtualenv()
    local('pep8 --config=conf/pep8_config.txt template_app | tee reports/template_app_pep8.txt; test ${PIPESTATUS[0]} -eq 0')
    local('pep8 --config=conf/pep8_config.txt django_template | tee reports/django_template_pep8.txt; test ${PIPESTATUS[0]} -eq 0')


def run_tests():
    _ensure_virtualenv()
    unit_test()
    copy_settings()
    local('coverage run manage.py test --noinput --with-coverage --cover-package=template_app --cover-min-percentage=86 --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml --cover-branches --exclude-dir=template_app/tests/py_integration')


def run_integration_tests():
    _ensure_virtualenv()
    unit_test()
    copy_settings()
    local('python manage.py test template_app.tests.py_integration --noinput')


def precommit():
    _ensure_virtualenv()
    install_all_deps()
    local('rm -rf reports')
    local('mkdir -p reports')
    pylint()
    pep8()
    run_tests()
    run_integration_tests()
