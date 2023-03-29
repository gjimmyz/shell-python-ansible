#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.ping_check.py
#Function:
#Version:1.0
#Created:2021-06-05
#--------------------------------------------------
import re
import subprocess
import os

fmt = '\033[0;3{}m{}\033[0m'.format
class color:
    RED    = 1#红
    GREEN  = 2#绿

cmd_ping = 'ping -c'
cmd_ping_count = '5 '
cmd_ping_timeout = '1 '
cmd_ping_args = '-w'
scripts_dir = "/root/scripts/"
ip_list = 'iplist.txt'
ip_list_path = os.path.join(scripts_dir,ip_list)
key_word = '100% packet loss'

def checkalive(ip):
    cmdline = cmd_ping + cmd_ping_count + cmd_ping_args + cmd_ping_timeout + ip
    print cmdline
    cmd_action = ((subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE)).stdout.read()).decode()
    result = re.findall(key_word,cmd_action)
    if len(result) == 0:
        print fmt(color.GREEN,'%s is up' % (ip))
    else:
        print fmt(color.RED,'%s is down' % (ip))

if __name__=="__main__":
    if os.path.exists(ip_list_path):
        with open(ip_list_path,'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                ip = line.strip()
                checkalive(ip)
    else:
       print '请检查%s文件是否存在' % (ip_list)
