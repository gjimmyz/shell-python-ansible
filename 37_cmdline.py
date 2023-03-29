#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.cmdline.py
#Function:
#Version:1.0
#Created:2021-05-28
#--------------------------------------------------
import os
import subprocess
import sys

cmd_wget = 'wget '
cmd_tar = 'tar -xf '
cmd_cd = 'cd '
cmd_ln = 'ln -s '
cmd_configure = './configure'
cmd_make = 'make'
cmd_install = 'make install'

url = "http://10.xxx.xxx.76/Python-3.9.5.tar.xz"
url_name = url.split('/')[-1]
tar_dest = "/root/scripts/python3_tar_bao"
tar_dest_file = os.path.join(tar_dest,url_name)
tar_dir = url_name.replace('.tar.xz','')
tar_dest_dir = os.path.join(tar_dest,tar_dir)

#暂时没用到
def action_subprocess(cmdline):
    cmd_action = subprocess.Popen(args=cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    while True:
        line = cmd_action.stdout.readline()
        if line == '' and cmd_action.poll() is not None:
            break
        sys.stdout.write(line)
        sys.stdout.flush()

#cmdline os system
def action_system(cmdline):
    cmd_action = os.system(cmdline)
    if cmd_action == 0:
        return cmd_action
    else:
        print('something is wrong')
        sys.exit(0)

path_exists = os.path.exists(tar_dest)
if path_exists:
    print ('请检查%s目录是否为空目录,是空目录的话清删除这个目录' % (tar_dest))
if not path_exists:
    os.makedirs(tar_dest)
    if not os.path.exists(tar_dest_file):
        print ('1、开始下载%s%s' % (cmd_wget,url))
        action_system(cmd_cd + tar_dest + '&&' + cmd_wget + url)
    if not os.path.exists(tar_dest_dir):
        print ('2、开始解压%s%s' % (cmd_tar,url_name))
        action_system(cmd_cd + tar_dest + '&&' + cmd_tar + url_name)
    if os.path.exists(tar_dest_dir):
        print ('3、快捷方式%s%s python3' % (cmd_ln,tar_dir))
        action_system(cmd_cd + tar_dest + '&&' + cmd_ln + tar_dir + " " + 'python3')
        print ('4、进入目录进行编译三部曲之一cd python3 && %s' % (cmd_configure))
        action_system(cmd_cd + tar_dest + '/' + 'python3' + '&&' + cmd_configure)
        print ('5、进入目录进行编译三部曲之二cd python3 && %s' % (cmd_make))
        action_system(cmd_cd + tar_dest + '/' + 'python3' + '&&' + cmd_make)
        print ('6、进入目录进行编译三部曲之三cd python3 && %s' % (cmd_install))
        action_system(cmd_cd + tar_dest + '/' + 'python3' + '&&' + cmd_install)
