#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.rsync_trans.py
#Function:
#Version:1.0
#Created:2021-06-01
#--------------------------------------------------
#yum -y install rsync
import pexpect
import time
import os
import sys

rsync_user = 'jenkins'
rsync_passwd = 'jenkins'
rsync_ip = '10.81.112.87'
rsync_module = 'jenkins'
rsync_log_dir = '/root/scripts/rsync_log'
rsync_dl_dir = '/opt/jenkins'
rsync_cmd = '/usr/bin/rsync'
rsync_limit = 50000
rsync_args = "-vartopg --progress --bwlimit=%s" % rsync_limit
rsync_log_file = time.strftime('%Y%m%d%H%M')

#同步数据到rsync_dl_dir
def rsync_bak():
    rsync_cmdline = "%s %s %s@%s::%s %s" % (rsync_cmd,rsync_args,rsync_user,rsync_ip,rsync_module,rsync_dl_dir)
    child = pexpect.spawn(rsync_cmdline)
    #打印下具体跑的命令等等
    print child.args
    #记录日志到文件
    path_exists = os.path.exists(rsync_log_dir)
    if not path_exists:
        os.makedirs(rsync_log_dir)
    fout = open(rsync_log_dir + "/" + rsync_log_file,'w')
    child.logfile = fout
    ret = child.expect(['[Pp]assword: ',pexpect.EOF,pexpect.TIMEOUT],timeout=30)
    if ret == 0:
      child.sendline(rsync_passwd)
    else:
      print '可以去rsync_log目录下看日志'
      sys.exit()
    return child.expect([pexpect.EOF,pexpect.TIMEOUT])
if __name__ == '__main__':
    rsync_bak()
