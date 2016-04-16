$project_name = "django_template"

$project_path = "/opt/$project_name"
$project_path_code = "$project_path/code"
$project_path_static = "$project_path/static"
$project_venv_path = "$project_path/venv"
$project_pip_reqs_path = "$project_path_code/dependencies/prod.txt"
$logs_path = "/var/log/$project_name"
$logs_path_test = "$logs_path/test"

$project_username = "dtuser"
$project_sudo_username = "dtsudo"
$project_common_groupname = "dtowners"
$project_userhome = "/home/$project_username"
$project_sudo_userhome = "/home/$project_sudo_username"

$db_name = "dtdb"
$db_name_selenium = "dtdb_selenium"
$db_username = "dtdb_user"
$db_password = "dtdb_password"


include epel
include repoforge


class { 'sudo':
    purge               => false,
    config_file_replace => false,
}


class privileges {
    sudo::conf { 'admins':
      content => '%admins ALL=(ALL) NOPASSWD: ALL',
    }
}
include privileges


class create_groups_users {
    
    group { $project_username:
        ensure => present,
        gid    => 1002
    }

    group { $project_common_groupname:
        ensure => present,
        gid    => 1003
    }

    group { $project_sudo_username:
        ensure => present,
        gid    => 1004
    }

    group { "admins":
        ensure => present,
        gid    => 1005
    }

    user { $project_username:
        ensure     => present,
        gid        => "1002",
        uid        => "1002",
        membership => minimum,
        require    => [Group[$project_common_groupname], Group[$project_username], Class["nginx"]],
        groups     => [$project_common_groupname, "nginx"],
        home       => $project_userhome,
        managehome => true,
    }
    
    user { $project_sudo_username:
        ensure     => present,
        gid        => "1004",
        uid        => "1004",
        membership => minimum,
        require    => [Group[$project_common_groupname], Group[$project_sudo_username],
                       Group["admins"], Class["privileges"], Class["nginx"]],
        groups     => [$project_common_groupname, "admins", "nginx"],
        home       => $project_sudo_userhome,
        managehome => true,
    }
}
include create_groups_users


class create_dirs {

    file { $project_path:
        ensure  => 'directory',
        owner   => $project_username,
        group   => $project_common_groupname,
        mode    => '0775',
        require => [User[$project_username], Group[$project_common_groupname]]
    }
    
    $other_dirs = [$project_path_code, $logs_path, "/home/$project_username/ssl"]
    file { $other_dirs:
        ensure  => 'directory',
        owner   => $project_username,
        group   => $project_common_groupname,
        mode    => '0775',
        require => [User[$project_username], Group[$project_common_groupname]]
    }
    
    file { $logs_path_test:
        ensure  => 'directory',
        owner   => $project_username,
        group   => $project_common_groupname,
        mode    => '0775',
        require => [User[$project_username], Group[$project_common_groupname],
                    File[$logs_path]]
    }
}
include create_dirs


class install_lib_deps {

    $project_libs = ["git", "nano", "gcc-c++", "net-tools", "wget", "epel-release"]
    package { $project_libs:
        ensure   => latest,
    }

    $secondary_libs = ["uwsgi", "uwsgi-plugin-python", "xorg-x11-server-Xvfb", "firefox.x86_64"]
    package { $secondary_libs:
        ensure   => latest,
        require  => [Package["epel-release"]]
    }
    
    package { "rubygems":
        ensure => installed,
    }
    
    package { "inifile":
        ensure   => installed,
        provider => "gem",
        require  => Package["rubygems"],
    }
}
include install_lib_deps


class clone_project {

    vcsrepo { $project_path_code:
        ensure   => present,
        provider => git,
        source   => 'git://github.com/mcjug2015/django_template.git',
        require  => [File[$project_path_code], Package["git"]],
        owner   => $project_username,
        group   => $project_common_groupname,
    }
}
include clone_project


class { 'nginx': }


class { 'python' :
    version    => 'system',
    pip        => 'latest',
    dev        => 'present',
    virtualenv => 'latest',
    gunicorn   => 'absent',
}


python::virtualenv { $project_venv_path:
    ensure       => present,
    version      => 'system',
    systempkgs   => true,
    distribute   => false,
    venv_dir     => $project_venv_path,
    owner        => $project_username,
    group        => $project_common_groupname,
    requirements => $project_pip_reqs_path,
    timeout      => 1800,
    require      => [Vcsrepo[$project_path_code], Class["postgresql::lib::devel"]]
}


class {'postgresql::globals':
    version => '9.5',
    manage_package_repo => true,
    encoding => 'UTF8',
    locale   => "en_US.UTF-8",
}->
class { 'postgresql::server':
    listen_addresses => '*',
}
class { 'postgresql::lib::devel':}
class setup_db {

    postgresql::server::role { $db_username:
        password_hash => postgresql_password($db_username, $db_password),
        superuser     => true
    }

    postgresql::server::db { $db_name:
        user     => $db_username,
        password => postgresql_password($db_username, $db_password),
    }

    postgresql::server::db { $db_name_selenium:
        user     => $db_username,
        password => postgresql_password($db_username, $db_password),
    }

    postgresql::server::database_grant { 'give_bits':
        privilege => 'ALL',
        db        => $db_name,
        role      => $db_username,
    }
    
    postgresql::server::database_grant { 'give_bits_selenium':
        privilege => 'ALL',
        db        => $db_name_selenium,
        role      => $db_username,
    }
    
    exec {"install postgis2":
        command => "/bin/yum -y install postgis2_95",
        group   => "root",
        user    => "root",
        creates => "/usr/pgsql-9.5/share/extension/postgis.control",
        require => [Class["repoforge"], Class["epel"], Postgresql::Server::Db[$db_name]],
    }
    
    exec {"install postgis extensions":
        command => "/usr/bin/psql $db_name -c \"CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;\"",
        group   => "postgres",
        user    => "postgres",
        require => [Exec["install postgis2"]],
        unless => "/usr/bin/psql -d $db_name -c '\\dx' | grep postgis",
    }
    
    exec {"install postgis extensions for selenium db":
        command => "/usr/bin/psql $db_name_selenium -c \"CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;\"",
        group   => "postgres",
        user    => "postgres",
        require => [Exec["install postgis2"]],
        unless => "/usr/bin/psql -d $db_name_selenium -c '\\dx' | grep postgis",
    }
}
include setup_db


openssl::certificate::x509 { "the_cert":
    ensure       => present,
    country      => "US",
    organization => "MCJUG2015",
    commonname   => "localhost",
    state        => "MD",
    locality     => "montgomery county",
    days         => 3456,
    base_dir     => "/home/$project_username/ssl",
    owner        => $project_username,
    group        => "nginx",
    force        => false,
    require      => [File["/home/$project_username/ssl"], Package["inifile"]],
}


class { "selinux":
    mode => "permissive",
    type => "targeted",
}


class final_setup {
    
    exec {"install node":
        command => "bash -c \"source $project_venv_path/bin/activate;fab one_time_node_install;\"",
        group   => $project_common_groupname,
        user    => $project_username,
        require => [Package["gcc-c++"], Python::Virtualenv[$project_venv_path],
                    Vcsrepo[$project_path_code]],
        unless  => "bash -c \"test -d $project_venv_path/lib/node_modules/npm\"",
        timeout => 1800,
        path    => "/opt/django_template/venv/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/home/dtuser/.local/bin:/home/dtuser/bin",
        cwd     => $project_path_code,
    }
    
    exec {"invoke tests":
        command => "bash -c \"source $project_venv_path/bin/activate;fab vagrant_test precommit\"",
        group   => $project_common_groupname,
        user    => $project_username,
        require => [Exec["install postgis extensions"], Exec["install node"]],
        path    => "/opt/django_template/venv/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/home/dtuser/.local/bin:/home/dtuser/bin",
        cwd     => $project_path_code,
    }
    
    exec {"do refresh":
        command => "bash -c \"source $project_venv_path/bin/activate;fab vagrant refresh_local\"",
        group   => $project_common_groupname,
        user    => $project_username,
        require => [Exec["invoke tests"], Class["selinux"]],
        path    => "/opt/django_template/venv/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/home/dtuser/.local/bin:/home/dtuser/bin",
        cwd     => $project_path_code,
    }
    
    exec {"do sudo_refresh":
        command => "bash -c \"source $project_venv_path/bin/activate;fab vagrant sudo_refresh_local\"",
        group   => $project_common_groupname,
        user    => $project_sudo_username,
        require => [Exec["do refresh"], ],
        path    => "/opt/django_template/venv/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/home/dtuser/.local/bin:/home/dtuser/bin",
        cwd     => $project_path_code,
    }
}
include final_setup