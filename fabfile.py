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


def vagrant_selenium():
    env.instance = 'vagrant_selenium'


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
    local('cp conf/uwsgi_params django_template/uwsgi_params' % env)


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
    local('coverage run manage.py test --noinput --with-coverage --cover-package=template_app --cover-min-percentage=86 --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml --cover-branches --exclude-dir=template_app/tests/py_integration --exclude-dir=template_app/tests/selenium --exe')


def run_selenium_tests():
    _ensure_virtualenv()
    require('instance')
    local('cp django_template/environments/%(instance)s/settings/%(instance)s_code.py django_template/settings.py' % env)
    local('python manage.py test --noinput --keepdb template_app.tests.selenium')


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


def copy_to_served():
    '''
        Lets keep the code uwsgi actually runs off separate from our sandbox,
        cleaner that way. For responsive development use runserver.
    '''
    _ensure_virtualenv()
    local("rm -rf /opt/django_template/served")
    local("cp -R /opt/django_template/code /opt/django_template/served")
    local("chown -R dtuser:nginx /opt/django_template/served")


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
    local('sudo cp conf/dt.conf /etc/nginx/sites-available/' % env)
    local('sudo rm -rf /etc/nginx/sites-enabled/dt.conf')
    local('sudo ln -s /etc/nginx/sites-available/dt.conf /etc/nginx/sites-enabled/dt.conf')


def update_static_files():
    local('rm -rf /opt/django_template/static/template_app')
    local('mkdir -p /opt/django_template/static/template_app')
    local('cp -r template_app/static/js /opt/django_template/static/')
    local('cp -r template_app/static/html /opt/django_template/static/')
    local('cp -r /opt/django_template/venv/lib/python2.7/site-packages/django/contrib/admin/static/admin /opt/django_template/static/')
    local('cp -r /opt/django_template/venv/lib/python2.7/site-packages/django/contrib/gis/static/gis /opt/django_template/static/')


def refresh_local():
    require('instance')
    _ensure_virtualenv()
    install_all_deps()
    copy_settings()
    copy_uwsgi_params()
    local('python manage.py migrate --noinput')
    update_static_files()
    copy_to_served()


def copy_uwsgi_ini():
    local('sudo cp conf/uwsgi.ini /etc/uwsgi.d/dt_uwsgi.ini' % env)
    local('sudo chown dtuser:nginx /etc/uwsgi.d/dt_uwsgi.ini' % env)


def reboot_all():
    with settings(warn_only=True):
        local('sudo systemctl stop nginx')
        local('sudo systemctl stop uwsgi')
    local('sudo systemctl start uwsgi')
    local('sudo systemctl start nginx')


def ensure_socket():
    local("sudo rm -rf /var/run/django_template/")
    local("sudo mkdir -p /var/run/django_template/")
    local("sudo chown -R dtuser:nginx /var/run/django_template/")


def put_root_uwsgi_ini():
    local("sudo cp conf/root_uwsgi.ini /etc/uwsgi.ini")


def put_uwsgi_systemd_file():
    local("sudo cp conf/uwsgi.service /usr/lib/systemd/system/uwsgi.service")
    local("sudo systemctl enable uwsgi")
    local("sudo systemctl daemon-reload")


def sudo_refresh_local():
    update_ngnix_conf()
    ensure_socket()
    copy_uwsgi_ini()
    put_root_uwsgi_ini()
    put_uwsgi_systemd_file()
    reboot_all()


def sudo_reset_db():
    local('''sudo su - postgres -c "/usr/bin/psql -c \\"SELECT pg_terminate_backend(pid) FROM  pg_stat_activity WHERE datname = 'dtdb_selenium';\\""''')
    local('''sudo su - postgres -c "/usr/bin/dropdb dtdb_selenium"''')
    local('''sudo su - postgres -c "/usr/bin/createdb dtdb_selenium"''')
    local('''sudo su - postgres -c "/usr/bin/psql dtdb_selenium -c \\"CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;\\""''')


def ensure_xvfb():
    local("sudo cp conf/xvfb.service /usr/lib/systemd/system/xvfb.service")
    local("sudo systemctl enable xvfb")
    local("sudo systemctl daemon-reload")


def ensure_selenium():
    local("sudo mkdir -p /opt/selenium-server/")
    local('''[ -f /opt/selenium-server/selenium-server.jar ] && echo "found selenium jar" || sudo wget http://selenium-release.storage.googleapis.com/2.53/selenium-server-standalone-2.53.0.jar -O /opt/selenium-server/selenium-server.jar''')
    local("sudo chown -R dtuser:dtowners /opt/selenium-server/")
    local("sudo cp conf/selenium-server.service /usr/lib/systemd/system/selenium-server.service")
    local("sudo systemctl enable selenium-server")
    local("sudo systemctl daemon-reload")


def start_selenium_services():
    local("sudo systemctl start xvfb")
    local("sudo systemctl start selenium-server")


def sudo_prepare_for_selenium():
    ensure_xvfb()
    ensure_selenium()
    start_selenium_services()
    sudo_refresh_local()
