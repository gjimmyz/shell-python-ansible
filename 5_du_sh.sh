#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:du_sh.sh
#Function:
#Version:1.0
#Created:2021-03-09
#--------------------------------------------------
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin
#currdate=$(date +%Y%m%d%H%M)
currdate=$(date +%Y%m%d)
scripts_dir="/root/scripts"
logfile="${scripts_dir}/du_log/${currdate}/du_sh.log"
function redirectlog ()
{
    exec 1>> ${logfile}
    exec 2>> ${logfile}
}
#----------日志重定向-------------------------------
#redirectlog

rsync_list_file=${scripts_dir}/list_file
file=${scripts_dir}/action_file

sync_dir="/opt/temp_mount/glusterfs/home"
all_dir_file_num=`cd ${sync_dir} && ls -1|wc -l`


if [[ ! -f ${rsync_list_file} ]]
then
    cd ${sync_dir} && ls -1 > ${rsync_list_file}
fi

if [[ -n ${rsync_list_file} ]] && [[ ${all_dir_file_num} -ne 0 ]]
then
    process_num=`ps -ef|grep -v grep|grep 'du -sh'|wc -l`
    para_num=10
    if [[ ${process_num} -le ${para_num} ]]
    then
        mkdir /root/scripts/du_log/${currdate} -pv
        redirectlog
        cat ${rsync_list_file}|head -n 1 > ${file}
        sed -i '1d' ${rsync_list_file}
        #cd ${sync_dir} && time du -sh `cat ${file}` >> /root/scripts/du_log/${currdate}/du_sh.log 2>&1
        if [[ -s ${file} ]]
        then
           cd ${sync_dir} && du -sh `cat ${file}`
        fi
    fi
fi
