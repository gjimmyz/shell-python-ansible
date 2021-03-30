#!/bin/bash
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:ansible_space_disk_check.sh
#Function:
#Version:1.0
#Created:2020-12-16
#--------------------------------------------------
set -o nounset
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin
currdate=$(date +%Y%m%d)
sleeptime="5"
scriptdir="/etc/ansible/ansible_check_all_space_log"
logfile="${scriptdir}/check_disk_space"
ansiblelog="${scriptdir}/disk_space_log"
ansiblemaillog="${scriptdir}/disk_space_mail_log"

function echofail ()
{
    echo "$1" 1>&2
    exit 1
}
#----------退出函数------------------------
function getip ()
{
    num0=$(ip a|grep -w ens192|wc -l)
    aliasip0="ens192"
    num1=$(ip a|grep -w eno4|wc -l)
    aliasip1="eno4"
    if [[ ${num1} != 0 ]]
    then
        ip a|grep ${aliasip1}|grep inet|awk '{print $2}'|awk -F"/" '{print $1}'
    else
        ip a|grep ${aliasip0}|grep inet|awk '{print $2}'|awk -F"/" '{print $1}'
    fi
}
#----------获得IP函数------------------------
function checkowner ()
{
    #可能修改的地方
    uname1="root"
    uname2=$(cat /etc/passwd|awk /^${uname1}/|awk -F: '{print $1}')
    if [[ ${uname1} != ${uname2} ]]
    then
        echofail "script need $uname1"
    fi
}
#----------检查id权限只有特定用户可以运行--------
function usage ()
{
    echo "Usage1:bash $(basename $0) start &"
}
#----------显示脚本如何运行----------------
if [[ $# -ne 1 ]]
then
    usage
    echofail "需要加参数"
fi
#----------检查参数---------------------------
function redirectlog ()
{
    exec 1> ${logfile}
    exec 2>> ${logfile}
}
#----------日志重定向-------------------------------
function getdiskspace ()
{
    ansible -i /etc/ansible/save_hosts dell_disk -m shell -a "df -hP|awk 'NR>=1 && int(\$5) > 90'"|awk '/CHANGED/{ip=$1;next}{print ip,$0}' > ${ansiblelog}
    ansible -i /etc/ansible/save_hosts hp_disk -m shell -a "df -hP|awk 'NR>=1 && int(\$5) > 90'"|awk '/CHANGED/{ip=$1;next}{print ip,$0}' >> ${ansiblelog}
    ansible -i /etc/ansible/save_hosts lenovo_disk -m shell -a "df -hP|awk 'NR>=1 && int(\$5) > 90'"|awk '/CHANGED/{ip=$1;next}{print ip,$0}' >> ${ansiblelog}
    ansible -i /etc/ansible/save_hosts vm_disk -m shell -a "df -hP|awk 'NR>=1 && int(\$5) > 90'"|awk '/CHANGED/{ip=$1;next}{print ip,$0}' >> ${ansiblelog}
    cat ${ansiblelog}|grep -wv "/dev/loop0"|grep -wv "/boot"|awk /dev/|awk '$2 !~/^$/{print $0}'|sort -nr -k6 > ${ansiblemaillog}
}
#----------通过ansible获取磁盘空间--------------------------
function main ()
{
    sed -i -e '1i\Ip\tFileSystem\tTotalSpace\tUseSpace\tFreeSpace\tFreePercent\tMount' ${ansiblemaillog}
    sed -i -e 's/^/<tr><td>/' -e 's/\s\+/<\/td><td>/' -e 's/\s\+/<\/td><td>/' -e 's/\s\+/<\/td><td>/' -e 's/\s\+/<\/td><td>/' -e 's/\s\+/<\/td><td>/' -e 's/\s\+/<\/td><td>/' -e 's/$/<\/td><\/tr>/' ${ansiblemaillog}
    sed -i -e '1i\<table>' -e '$a\</table>' ${ansiblemaillog}
    sed -i -e '1i\<style type="text\/css">table,td,th{border:1px solid black;}<\/style>' ${ansiblemaillog}
}
#----------主函数--------------------------
function handlemail ()
{
    python ${scriptdir}/mailsend_20201123.py ${ansiblemaillog} "$0 $(getip)"
}
#----------发送邮件-----------------------
redirectlog
checkowner
getdiskspace
main
handlemail
