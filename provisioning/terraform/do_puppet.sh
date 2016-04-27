#!/bin/bash


# install puppet agent and modules. this will be invoked by cloud init.
/usr/bin/rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
/usr/bin/yum -y install puppet
/usr/bin/puppet module install stahnma-epel
/usr/bin/puppet module install m0byd1ck-repoforge
/usr/bin/puppet module install puppetlabs-postgresql
/usr/bin/puppet module install stankevich-python
/usr/bin/puppet module install puppetlabs-vcsrepo
/usr/bin/puppet module install jfryman-nginx
/usr/bin/puppet module install saz-sudo
/usr/bin/puppet module install jfryman-selinux

/usr/bin/puppet apply /tmp/django_template/provisioning/vagrant/environments/default/manifests/site.pp