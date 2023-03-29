#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:destroy_lxc_after_shutdown.sh
#Function:
#Version:1.0
#Created:2022-12-13
#--------------------------------------------------
#source https://forum.proxmox.com/threads/pct-exec-direct-into-lxc-guest.116726/
if [ "$2" == "pre-start" ]
then
    echo "Lxc $1 will self-destruct after shutdown!"
elif [ "$2" == "post-stop" ]
then
    nohup /usr/sbin/pct destroy "$1" &>/dev/null &
fi
