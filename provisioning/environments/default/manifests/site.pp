$dt_user_home = "/home/dtuser/"
$dt_sudo_home = "/home/dtsudo/"


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


class create_groups_users_dirs {
    
    group { "dtuser":
        ensure => present,
        gid    => 1002
    }

    group { "dtowners":
        ensure => present,
        gid    => 1003
    }

    group { "dtsudo":
        ensure => present,
        gid    => 1004
    }

    group { "admins":
        ensure => present,
        gid    => 1005
    }

    user { "dtuser":
        ensure     => present,
        gid        => "1002",
        uid        => "1002",
        membership => minimum,
        require    => [Group["dtowners"], Group["dtuser"]],
        groups     => ["dtowners"],
        home       => $dt_user_home,
        managehome => true,
    }
    
    user { "dtsudo":
        ensure     => present,
        gid        => "1004",
        uid        => "1004",
        membership => minimum,
        require    => [Group["dtowners"], Group["dtsudo"], Group["admins"], Class["privileges"]],
        groups     => ["dtowners", "admins"],
        home       => $dt_sudo_home,
        managehome => true,
    }
}
include create_groups_users_dirs