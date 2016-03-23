# django_template
A template django project

If "vagrant up" fails, try "ulimit -n 4048;vagrant up;". Might start working after that.
https://github.com/mitchellh/vagrant/issues/2435 and http://stackoverflow.com/questions/18808540/error-when-running-vagrant-up-too-many-open-files-getcwd-errnoemfile have some insight, but not much.

After vagrant up, apply migrations and do python manage.py runserver 192.168.50.4:8000 to get
a test server accessible from the host going.

Initial creds are admin/admin. http://192.168.50.4:8000/admin/ and http://192.168.50.4:8000/welcome/ can be visited.


To query cigar shops by lat, long, and distance in miles do:
http://127.0.0.1:8000/api/v1/cigarshop/?lat=37.067922&long=-75.130205&distance=10&format=json

Fixture test_user password is testing123

Example run_list invocation
python manage.py run_list '/home/dtuser/Desktop/latest_meetings.txt' '/opt/django_template/code/reports/load_meetings_err.txt' '/opt/django_template/code/reports/load_meetings_err_detail.txt'


uwsgi/ngnix stuff - after sudo_refresh_local do "uwsgi --socket :8000 --module django_template.wsgi" for uwsgi to start
chooching. will demonize soon.