#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gongzheng
#Email:85646830@qq.com
#FileName:webapp_update.py
#Function: 
#Version:1.0 
#Created:2020-04-25
#--------------------------------------------------
import time
import shutil

#Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。
#time.strftime(format[, t]) 
#time.strftime(format)
#https://docs.python.org/2/library/time.html
time_file=time.strftime('%Y%m%d%H%M')

site_dir="zex_web"
update_file="/tmp/zex_web_upload/" + site_dir + ".jar"
webapp_file="/home/gjimmyz/zex/" + site_dir + ".jar"
webapp_bak_file="/home/gjimmyz/zex_bak/" + site_dir + ".jar_" + time_file

#https://docs.python.org/2/library/shutil.html
#shutil.copyfile(src, dst)
#Copy the contents (no metadata) of the file named src to a file named dst. dst must be the complete target file name; look at shutil.copy() for a copy that accepts a target directory path. If src and dst are the same files, Error is raised. The destination location must be writable; otherwise, an IOError exception will be raised. If dst already exists, it will be replaced. Special files such as character or block devices and pipes cannot be copied with this function. src and dst are path names given as strings.
shutil.copyfile(webapp_file,webapp_bak_file)
print ("copy file ok")
shutil.copyfile(update_file,webapp_file)
print ("update file ok")

效果:
[gjimmyz@localhost scripts]$ python zex_update.py
copy file ok
update file ok

[root@localhost zex]# ll /home/gjimmyz/zex_bak/
total 131584
-rw-rw-r-- 1 gjimmyz gjimmyz  1122722 Apr 25 10:24 zex_web.jar_202004251024
-rw-rw-r-- 1 gjimmyz gjimmyz  1122722 Apr 25 10:27 zex_web.jar_202004251027
-rw-rw-r-- 1 gjimmyz gjimmyz 66241734 Apr 25 10:28 zex_web.jar_202004251028
-rw-rw-r-- 1 gjimmyz gjimmyz 66241734 Apr 25 10:29 zex_web.jar_202004251029

参考:
https://docs.python.org/2/library/shutil.html
https://docs.python.org/2/library/time.html
