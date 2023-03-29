#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:du_usage_3.py
#Function:
#Version:1.0
#Created:2021-04-07
#--------------------------------------------------
#https://docs.python.org/2/library/subprocess.html#subprocess.Popen.communicate
#https://stackoverflow.com/questions/16642681/whats-the-difference-between-communicate-and-communicate0
#https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes
import subprocess
import time

cmd_titan = "du -shc /opt/temp_mount/titan/*"
output_titan = subprocess.check_output(["bash","-c",cmd_titan])

time_file=time.strftime('%Y%m%d')

out_file_titan="/root/scripts/du_log/titan/" + time_file + ".log"
with open(out_file_titan,'w') as f:
   f.write(output_titan)
