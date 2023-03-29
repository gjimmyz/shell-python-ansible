#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.scan_ip.py
#Function:
#Version:1.0
#Created:2021-06-03
#--------------------------------------------------
import socket
import sys
from datetime import datetime
import os

scripts_dir = "/root/scripts/"
ip_list = 'iplist.txt'
ip_list_path = os.path.join(scripts_dir,ip_list)

#扫描xx ip的端口
def socket_scan(remote_ip,remote_port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ret_num = s.connect_ex((remote_ip,remote_port))
    if ret_num == 0:
        print "Port %d:OPEN" % remote_port
    s.close()

if __name__ =="__main__":
   t1 = datetime.now()
   if os.path.exists(ip_list_path):
       with open(ip_list_path,'r') as f:
         while True:
           line = f.readline()
           if len(line) == 0:
               break
           remote_ip = line.strip()
           print remote_ip
           for remote_port in range(1,65535):
               socket_scan(remote_ip,remote_port)
       t2 = datetime.now()
       total = t2 - t1
       print 'Total Time:',total
   else:
       print '请检查iplist.txt文件是否存在'

cat iplist.txt
10.81.112.86
10.81.112.87
