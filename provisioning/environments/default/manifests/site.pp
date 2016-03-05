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
$db_username = "dtdb_user"
$db_password = "dtdb_password"


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
        require    => [Group[$project_common_groupname], Group[$project_username]],
        groups     => [$project_common_groupname],
        home       => $project_userhome,
        managehome => true,
    }
    
    user { $project_sudo_username:
        ensure     => present,
        gid        => "1004",
        uid        => "1004",
        membership => minimum,
        require    => [Group[$project_common_groupname], Group[$project_sudo_username],
                       Group["admins"], Class["privileges"]],
        groups     => [$project_common_groupname, "admins"],
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
    
    $other_dirs = [$project_path_code, $logs_path]
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

    $project_libs = ["git", "postgresql-devel"]
    package { $project_libs:
        ensure => latest,
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

    file { $project_path_static:
        ensure  => 'directory',
        owner   => $project_username,
        group   => $project_common_groupname,
        mode    => '0775',
        require => [User[$project_username], Group[$project_common_groupname],
                    Vcsrepo[$project_path_code], File[$project_path]],
        source  => "file://$project_path_code/template_app/static",
        recurse => true,
    }
}
include clone_project


class { 'nginx': }
class setup_nginx {

    nginx::resource::vhost { 'localhost':
        www_root => $project_path_static,
    }

}
include setup_nginx


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
    require      => [Vcsrepo[$project_path_code], Package["postgresql-devel"]]
}


class { 'postgresql::server': }
class setup_db {

    postgresql::server::role { 'dtdb_user':
        password_hash => postgresql_password('dtdb_user', 'dtdb_password'),
        superuser     => true
    }

    postgresql::server::db { "dtdb":
        user     => "dtdb_user",
        password => postgresql_password("dtdb_user", "dtdb_password"),
    }

    postgresql::server::database_grant { 'give_bits':
        privilege => 'ALL',
        db        => "dtdb",
        role      => "dtdb_user",
    }
}
include setup_db