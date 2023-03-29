#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.telnet_check.py
#Function:
#Version:1.0
#Created:2021-06-08
#--------------------------------------------------
import telnetlib
import os

fmt = '\033[0;3{}m{}\033[0m'.format
class color:
    RED    = 1#红
    GREEN  = 2#绿

scripts_dir = "/root/scripts/"
ip_list = 'iplist.txt'
ip_list_path = os.path.join(scripts_dir,ip_list)

def attempt(remote_ip,remote_port,timeout):
    try:
        telnet_lib = telnetlib.Telnet(remote_ip,remote_port,timeout)
        telnet_lib.open(remote_ip,remote_port,timeout)
        issue = telnet_lib.read_some()
        telnet_lib.close()
        print fmt(color.GREEN,'%s port %d is open' % (remote_ip,remote_port))
    except Exception as inst:
        error_reason = inst.args
        if inst.args[0] == "timed out":
            print fmt(color.RED,'%s port %d is %s' % (remote_ip,remote_port,inst.args[0]))

if __name__=="__main__":
    if os.path.exists(ip_list_path):
        with open(ip_list_path,'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                remote_ip = line.strip()
                remote_port = 22
                timeout = 5
                attempt(remote_ip,remote_port,timeout)
    else:
       print '请检查%s文件是否存在' % (ip_list)
