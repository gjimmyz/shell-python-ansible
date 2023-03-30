#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:save.sh
#Function:
#Version:1.0
#Created:2020-09-02
#--------------------------------------------------
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin
currdate=$(date +%Y%m%d%H%M)

mkdir -pv /root/scripts/save_backup/${currdate}
cd /root/scripts/save_backup/${currdate}
netstat -tupnl > netstat_${currdate}
ip a > ip_${currdate}
route -n > route_${currdate}
ip route > ip_route_${currdate}
df -Th > df_${currdate}
docker ps > docker_${currdate}
ps -aux > ps_${currdate}
uptime > uptime_${currdate}
crontab -l > crontab_${currdate}
ifconfig > ifconfig_${currdate}
hpssacli ctrl all show config > hpssacli_${currdate}
cd /opt/MegaRAID/MegaCli/ && ./MegaCli64 -ShowSummary -aALL > /root/scripts/save_backup/${currdate}/megaraid_${currdate}
