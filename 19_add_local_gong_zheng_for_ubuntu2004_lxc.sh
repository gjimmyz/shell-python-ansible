#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:add_local_gong_zheng_for_ubuntu2004_lxc.sh
#Function:
#Version:1.0
#Created:2022-12-13
#--------------------------------------------------
user="local_gong_zheng"
user_id="5091"
group_id="5091"
num=`cat /etc/passwd|grep 'local_*'|wc -l`

if [[ ${num} -eq 0 ]]
then
    groupadd -g ${group_id} ${user}
    useradd -s /bin/bash -d /home/${user} -m ${user} -u ${user_id} -g ${user_id}
    echo ${user}:${user}|chpasswd
    usermod -G docker ${user}
    echo "${user} ALL = (root) NOPASSWD:ALL"|tee /etc/sudoers.d/${user}
    chmod 0440 /etc/sudoers.d/${user}
    apt-get remove apparmor -y
else
    echo "111"
fi
