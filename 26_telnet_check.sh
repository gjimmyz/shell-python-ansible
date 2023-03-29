#!/bin/bash
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:telnet_check.sh
#Function:
#Version:1.0
#Created:2022-06-24
#--------------------------------------------------
set -o nounset
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin
port="8080"

function check_telnet ()
{
while [ 1 -ne 2 ]
do
    #yum -y install telnet
    echo  -e  "\n"|telnet $1 ${port}|grep -i connected >> /dev/null
    if [[ $? -eq 0 ]]
    then
        date >> telnet_$1.log
        echo "PORT OK" >> telnet_$1.log
    else
        date >> telnet_$1.log
        echo "PORT FALSE" >> telnet_$1.log
    fi
        sleep 1
done
}


for ip in $(cat iplist.txt)
do
{
    check_telnet ${ip}
} &
done

wait

#后台运行
#nohup bash telnet_check.sh &

cat iplist.txt
192.168.109.3
192.168.109.4
