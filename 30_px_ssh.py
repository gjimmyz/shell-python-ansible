#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.px_ssh.py
#Function:
#Version:1.0
#Created:2021-06-18
#--------------------------------------------------
import socket
from pexpect import pxssh
import os

fmt = '\033[0;3{}m{}\033[0m'.format
class color:
    RED    = 1#红
    GREEN  = 2#绿

scripts_dir = "/root/scripts/"
ip_list = 'iplist.txt'
ip_list_path = os.path.join(scripts_dir,ip_list)
ssh_username = 'user'
ssh_passwd = 'user'

#使用socket检查连接情况
def action(ssh_ip,ssh_port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #加了超时时间10s
    s.settimeout(10)
    return_num = s.connect_ex((ssh_ip,ssh_port))
    if return_num == 0:
        print fmt(color.GREEN,'ssh_ip:%s 连接正常,ssh_port:%d 端口已开放' % (ssh_ip,ssh_port))
        return return_num
    else:
        print fmt(color.RED,'ssh_ip:%s 连接失败或ssh_port:%d 端口没开放' % (ssh_ip,ssh_port))
    s.close()

if __name__=="__main__":
    if os.path.exists(ip_list_path):
        with open(ip_list_path,'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                ssh_ip = line.strip()
                ssh_port = 22
                if action(ssh_ip,ssh_port) == 0:
                    s = pxssh.pxssh()
                    s.login (ssh_ip,ssh_username,ssh_passwd)
                    s.sendline ('uptime')
                    s.prompt()
                    print s.before
    else:
       print '请检查%s文件是否存在' % (ip_list)
