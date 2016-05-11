# django_template

A template django project

Initial creds are admin/admin.

## local installation
```
git clone https://github.com/mcjug2015/django_template.git
cd django_template/provisioning/vagrant
ulimit -n 4048;vagrant up;
```
host machine http://192.168.50.4/admin/ and http://192.168.50.4/welcome/ can be visited after vagrant up.
To query cigar shops by lat, long, and distance in miles do:
http://192.168.50.4/api/v1/cigarshop/?lat=37.067922&long=-75.130205&distance=10&format=json

## remote installation
### aws
```
git clone https://github.com/mcjug2015/django_template.git
cd django_template/provisioning/terraform/aws
```
At this point you'll need to open up the dt_aws.tf file and put in your keys, local ip address, and aws keypair name. If you change the region you'll need to change the ami in the aws_instance section. We're based off of the official Centos 7 HVM ami. After that do:
```
terraform plan -out the_plan
terraform apply the_plan
terraform show
```
The last command will show you the public ip of the aws_instance that got created. The terraform script completes before the cloud init script finishes. ssh and tail /var/log/cloud-init-output.log, or wait ~15 minutes, the app will be up and running. After that you can go to ec2-...com/welcome/ and ec2-...com/admin/; The site forwards to 443 uses a self signed cert so you'll need to add an exception when your browser complains.


## Useful bits
If you modified stuff and wanna see it show up, or ran selenium tests or a precommit do
```
ssh to local or remote box as user with sudo bits

sudo su - dtuser
sg dtowners
source /opt/django_template/venv/bin/activate
cd /opt/django_template/code
fab vagrant refresh_local
```
and
```
ssh to local or remote box as user with sudo bits

sudo su - dtsudo
sg dtowners
source /opt/django_template/venv/bin/activate
cd /opt/django_template/code
fab vagrant sudo_refresh_local
```
This will make the box start hosting the regular site again.


## Advanced


Fixture test_user password is testing123


Example run_list invocation
```
python manage.py run_list '/home/dtuser/Desktop/latest_meetings.txt' '/opt/django_template/code/reports/load_meetings_err.txt' '/opt/django_template/code/reports/load_meetings_err_detail.txt'
```

Invoke seleniums with(might wanna do it from 2 terminal windows):
```
ssh to local or remote box as user with sudo bits

sudo su - dtuser
sg dtowners
source /opt/django_template/venv/bin/activate
cd /opt/django_template/code/
fab vagrant_selenium refresh_local
exit
exit
sudo su - dtsudo
sg dtowners
source /opt/django_template/venv/bin/activate
cd /opt/django_template/code/
fab sudo_prepare_for_selenium
exit
exit
sudo su - dtuser
sg dtowners
source /opt/django_template/venv/bin/activate
cd /opt/django_template/code/
fab vagrant_selenium run_selenium_tests
```
