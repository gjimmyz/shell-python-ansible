#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:test_py.py
#Function:
#Version:1.0
#Created:2021-04-09
#--------------------------------------------------
import subprocess

cmd_rpm = "rpm -qa|grep net-tools"
cmd_result = ((subprocess.Popen(cmd_rpm,shell=True,stdout=subprocess.PIPE)).stdout.read()).decode()
#len(str)# 字符串长度
if len(cmd_result) == 0:
    print ("net-tools no exists")
else:
    #strip()出去空行
    print (cmd_result.strip())

python test_py.py
net-tools-2.0-0.17.20131004git.el7.x86_64
