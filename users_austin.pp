user { "austin":
        uid => "1117",
        ensure => present,
        gid => "austin",
        membership => minimum,
        shell => "/bin/bash",
        home => "/home/austin",
}

group { "austin":
        gid => 1117,
}

# Ensure the home directory exists with the right permissions
file { "/home/austin":
	ensure => directory,
	owner => austin,
	group => austin,
	mode => '0755',
	require => [ User[austin], Group[austin] ],
}
 
# Ensure the .ssh directory exists with the right permissions
file { "/home/austin/.ssh":
	ensure => directory,
	owner => austin,
	group => austin,
	mode => '0700',
	require => File["/home/austin"],
} 

ssh_authorized_key { "austin":
        ensure => present,
        name => "austin",
        user => "austin",
        type => 'ssh-dss',
        key => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQC1f8pzhKMcgDJk83G2KFc8hH7mt68w8aGA8VVMQ8QXPAS18sxYT2LU0xHTwK0ceDn7JXMltPU9xKDw0i3xJenbZiSDjW/F0Piohadf6dsIb1rWp/tQbR/mWFoJllgNBgMuxqVxc2alQblzu14LksRsbNl0PSzD6iV2RDiactzbnBEUE6j2vCkas0r9XybCcKrdPKysnjmYbik/p86JX50Swn0/A/+Qipt9UxAdPhuipyjNvlpPLBYaAt6oLz9xMPqiuRLbRujAZry+3OaVxyNIE4cD94Nn/d0CyvdziCU0yKOoG2N4/ssIiak4i+3VQrtpSVdD5MZEhuODqwKxCqV5',
}
