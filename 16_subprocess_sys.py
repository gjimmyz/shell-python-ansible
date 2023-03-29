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
import sys

curl_cmd="curl -q -I https://www.mingmatechs.com|grep 'HTTP/1.1 200 OK'"
cmd_result = ((subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE)).stdout.read()).decode()
#python判断某个字符串中是否包含某个子字符串
if 'HTTP/1.1 200 OK' in str(cmd_result):
   print ("web is ok")
else:
   print ("web is not ok")
   sys.exit(1)
