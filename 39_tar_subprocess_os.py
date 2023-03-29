#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:dl_tar.py
#Function:
#Version:1.0
#Created:2021-05-19
#--------------------------------------------------
import os
import tarfile
import subprocess

url = "http://10.xxx.xxx.76/rpm.tar.gz"
url_name = url.split('/')[-1]
tar_dest = "/root/scripts/rpm_install"
tar_dest_name = os.path.join(tar_dest,url_name)
path_exists = os.path.exists(tar_dest)
if not path_exists:
    os.makedirs(tar_dest)
if not os.path.exists(tar_dest_name):
    cmd_curl = "curl"
    download = cmd_curl + " " + url + " " + "-o" + " " + tar_dest_name
    print download
    cmd_action = ((subprocess.Popen(download,shell=True,stdout=subprocess.PIPE)).stdout.read()).decode()
    result = os.system(cmd_action)
    if result is not 0:
        print("请检查cmd_action")
    else:
        tarfile.open(tar_dest_name,'r:gz').extractall(tar_dest)
