#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:mtr_monitor.sh
#Function:
#Version:1.0
#Created:2021-02-08
#--------------------------------------------------
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin
#currdate=$(date +%Y%m%d%H%M)
currdate=$(date +%Y%m%d)
scripts_dir="/root/scripts/"

report=${scripts_dir}/mtr_log/report_${currdate}
> ${report}

while read line
do
   mtr_num=`mtr -r -n -c 5 $line|wc -l`
   mtr_num1=`mtr -r -n -c 5 $line|grep "?"|wc -l`
   if [[ ${mtr_num} -eq 2 ]]
   then
      echo =====$line===== >> $report
   elif [[ ${mtr_num1} -eq 1 ]]
   then
      echo =====$line===== >> $report
   fi
done < ${scripts_dir}/iplist_all.txt

num=$(cat ${report}|wc -l)
if [[ ${num} -eq 0 ]]
then
    echo "no no no"
else
    cat ${report} > ${scripts_dir}/mtr_log/mtr_report
    cd /root/scripts && cat ${scripts_dir}/mtr_log/mtr_report|mail -s "mtr report" -r gongzheng@mingmatechs.com gong_zheng@mingmatechs.com
fi
