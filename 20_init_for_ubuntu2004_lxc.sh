#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:init_for_ubuntu2004_lxc.sh
#Function:
#Version:1.0
#Created:2022-12-13
#--------------------------------------------------
if [[ -f /usr/share/keyrings/docker-archive-keyring.gpg ]]
then
    echo "111"
else
    /usr/bin/wget http://xxx.xxx.xxx.xxx/init_for_ubuntu2004_lxc_conf/docker-archive-keyring.gpg -P /usr/share/keyrings/
    cd /etc/apt && rm -f sources.list && /usr/bin/wget http://xxx.xxx.xxx.xxx/init_for_ubuntu2004_lxc_conf/sources.list
    apt-get update
    apt-get -y install locales
    locale-gen en_US.UTF-8
    apt-get -y install tree net-tools docker-ce docker-ce-cli containerd.io vim openssh-server python3-pip
    systemctl enable docker
    /bin/sed -i 's/PasswordAuthentication no/#PasswordAuthentication yes/' /etc/ssh/sshd_config
    /bin/sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
    /bin/sed -i 's/#UseDNS no/UseDNS no/' /etc/ssh/sshd_config
    #systemctl restart sshd
    echo root:password |chpasswd
    rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    mkdir -pv /root/.pip && cd /root/.pip && /usr/bin/wget http://xxx.xxx.xxx.xxx/init_for_ubuntu2004_lxc_conf/.pip.conf
    pip3 install docker-compose --default-timeout=100
    if [[ ! -f /usr/local/bin/docker-compose ]]
    then
        /usr/bin/wget http://xxx.xxx.xxx.xxx/init_for_ubuntu2004_lxc_conf/docker-compose
    fi
    cd /etc/docker && /usr/bin/wget http://xxx.xxx.xxx.xxx/init_for_ubuntu2004_lxc_conf/daemon.json
    apt-get remove apparmor -y
    poweroff
fi
