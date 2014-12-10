user { "chris":
        uid => "1117",
        ensure => present,
        gid => "chris",
        membership => minimum,
        shell => "/bin/bash",
        home => "/home/chris",
}

group { "chris":
        gid => 1117,
}

ssh_authorized_key { "chris":
        ensure => present,
        name => "chris",
        user => "chris",
        type => 'ssh-dss',
        key => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQC1f8pzhKMcgDJk83G2KFc8hH7mt68w8aGA8VVMQ8QXPAS18sxYT2LU0xHTwK0ceDn7JXMltPU9xKDw0i3xJenbZiSDjW/F0Piohadf6dsIb1rWp/tQbR/mWFoJllgNBgMuxqVxc2alQblzu14LksRsbNl0PSzD6iV2RDiactzbnBEUE6j2vCkas0r9XybCcKrdPKysnjmYbik/p86JX50Swn0/A/+Qipt9UxAdPhuipyjNvlpPLBYaAt6oLz9xMPqiuRLbRujAZry+3OaVxyNIE4cD94Nn/d0CyvdziCU0yKOoG2N4/ssIiak4i+3VQrtpSVdD5MZEhuODqwKxCqV5',
}
