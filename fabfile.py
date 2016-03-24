#!/usr/bin/env python
from fabric.api import env, local, sudo, require, run, put, settings, cd, lcd
import os
import sys
from fabric.context_managers import warn_only


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


def vagrant():
    env.instance = 'vagrant'


def vagrant_test():
    env.instance = 'vagrant_test'


def _ensure_virtualenv():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found. Make sure to activate virtualenv first\n\n")
        sys.exit(-1)
    env.virtualenv = os.environ["VIRTUAL_ENV"]


def copy_settings():
    require('instance')
    local('cp django_template/environments/%(instance)s/settings/%(instance)s.py django_template/settings.py' % env)


def copy_uwsgi_params():
    require('instance')
    local('cp django_template/environments/%(instance)s/uwsgi_conf/uwsgi_params django_template/uwsgi_params' % env)


def copy_uwsgi_ini():
    require('instance')
    local('cp django_template/environments/%(instance)s/uwsgi_conf/uwsgi.ini django_template/uwsgi.ini' % env)


def install_prod_deps():
    _ensure_virtualenv()
    local('pip install -q -r dependencies/prod.txt' % env)


def install_all_deps():
    _ensure_virtualenv()
    install_prod_deps()
    local('pip install -q -r dependencies/dev.txt' % env)
    with lcd('template_app/front_end_qc'):
        local('npm install')


def pylint():
    _ensure_virtualenv()
    local('pylint --rcfile=conf/pylintrc.txt template_app | tee reports/template_app_pylint.txt; test ${PIPESTATUS[0]} -eq 0')
    local('pylint --rcfile=conf/pylintrc.txt django_template | tee reports/django_template_pylint.txt; test ${PIPESTATUS[0]} -eq 0')


def pep8():
    _ensure_virtualenv()
    local('pep8 --config=conf/pep8_config.txt template_app --exclude=front_end_qc | tee reports/template_app_pep8.txt; test ${PIPESTATUS[0]} -eq 0')
    local('pep8 --config=conf/pep8_config.txt django_template | tee reports/django_template_pep8.txt; test ${PIPESTATUS[0]} -eq 0')


def run_tests():
    require('instance')
    _ensure_virtualenv()
    copy_settings()
    local('coverage run manage.py test --noinput --with-coverage --cover-package=template_app --cover-min-percentage=86 --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml --cover-branches --exclude-dir=template_app/tests/py_integration --exe')


def run_integration_tests():
    require('instance')
    _ensure_virtualenv()
    copy_settings()
    local('python manage.py test template_app.tests.py_integration --noinput --exe')


def jshint():
    _ensure_virtualenv()
    with lcd('template_app/front_end_qc'):
        local('npm run jshint')


def jasmine():
    _ensure_virtualenv()
    with lcd('template_app/front_end_qc'):
        local('npm run jasmine')


def jasmine_stay_on():
    _ensure_virtualenv()
    with lcd('template_app/front_end_qc'):
        local('npm run jasmine_stay_on')


def precommit():
    require('instance')
    _ensure_virtualenv()
    install_all_deps()
    local('rm -rf reports')
    local('mkdir -p reports')
    pylint()
    pep8()
    jshint()
    run_tests()
    run_integration_tests()
    jasmine()


def update_ngnix_conf():
    require('instance')
    local('sudo cp django_template/environments/%(instance)s/ngnix_conf/dt.conf /etc/nginx/sites-available/' % env)
    local('sudo rm -rf /etc/nginx/sites-enabled/dt.conf')
    local('sudo ln -s /etc/nginx/sites-available/dt.conf /etc/nginx/sites-enabled/dt.conf')


def update_static_files():
    local('rm -rf /opt/django_template/static/template_app')
    local('mkdir -p /opt/django_template/static/template_app')
    local('cp -r template_app/static/js /opt/django_template/static/')
    local('cp -r template_app/static/html /opt/django_template/static/')


def refresh_local():
    require('instance')
    _ensure_virtualenv()
    install_all_deps()
    copy_settings()
    copy_uwsgi_params()
    copy_uwsgi_ini()
    local('python manage.py migrate --noinput')
    update_static_files()


def reboot_all():
    with settings(warn_only=True):
        local('sudo systemctl stop nginx')
    local('sudo systemctl start nginx')


def ensure_socket():
    local("sudo rm -rf /var/run/django_template/")
    local("sudo mkdir -p /var/run/django_template/")
    local("sudo chown -R dtuser:dtowners /var/run/django_template/")


def sudo_refresh_local():
    update_ngnix_conf()
    ensure_socket()
    reboot_all()
