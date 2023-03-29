#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:1.py
#Function:
#Version:1.0
#Created:2021-04-07
#--------------------------------------------------
#http://amoffat.github.io/sh/sections/piping.html
#http://amoffat.github.io/sh/sections/redirection.html#filename
#yum -y install python-pip
#cd /root/python_packages && pip install --no-index --find-links=file:. -r python_module.txt

import sh
import time

time_file=time.strftime('%Y%m%d')

list_dir_titan="/opt/temp_mount/titan/*"
list_dir_home="/opt/temp_mount/glusterfs/home/*"

out_file_titan="/root/scripts/du_log/titan/" + time_file + ".log"
out_file_home="/root/scripts/du_log/home/" + time_file + ".log"

list_glob_titan=sh.glob(list_dir_titan)
list_glob_home=sh.glob(list_dir_home)

(sh.du(list_glob_titan,'-shc',_out=out_file_titan))
(sh.du(list_glob_home,'-shc',_out=out_file_home))
