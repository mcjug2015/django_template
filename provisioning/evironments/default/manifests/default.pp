$dt_user_home = "/home/dtuser/"

class create_groups_users_dirs {
    group { "dtuser":
        ensure => present,
        gid    => 1002
    }

    group { "dtowners":
        ensure => present,
        gid    => 1003
    }

    user { "dtuser":
        ensure     => present,
        gid        => "1002",
        uid        => "1002",
        membership => minimum,
        require    => Group["dtowners"],
        groups     => ["1003"],
        home       => $dt_user_home,
        managehome => true,
    }
}
include create_groups_users_dirs