#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.analysis_uptime_log.py
#Function:
#Version:1.0
#Created:2021-04-29
#--------------------------------------------------
import os
import time

'''
https://docs.python.org/2/library/time.html
https://docs.python.org/2/library/os.html
/root/fetch_all_log和/root/scripts/analysis_log 2个目录已有
root用户运行的
分析文件是uptime_20210429
'''

time_file = time.strftime('%Y%m%d')
fetch_log = "/root/fetch_all_log/"
fetch_log_path = os.path.join(fetch_log,time_file)
analysis_log = "/root/scripts/analysis_log/"
analysis_log_path = os.path.join(analysis_log,time_file)
action_file = "uptime_" + time_file
result_file = analysis_log_path + "/" + "result.log"
mail_file = analysis_log_path + "/" + "mail_send"

#如果目录不存在 就创建目录
path_exists = os.path.exists(analysis_log_path)
if not path_exists:
    os.makedirs(analysis_log_path)

#文件存在 就清空下
if os.path.exists(result_file):
    with open(result_file,'r+') as f:
        f.truncate(0)
if os.path.exists(mail_file):
    with open(mail_file,'r+') as f:
        f.truncate(0)

#先找出具体文件路径 然后逐行打开 最后写入文件
for f in os.listdir(fetch_log_path):
    list_dir_name = os.path.join(fetch_log_path,f)
    file_path = os.path.join(list_dir_name,action_file)
    with open(file_path,'r') as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            contents = line.strip()
    with open(result_file,'a') as f:
        f.write(contents +"\n")

#对文件指定某列进行排序处理 并将需要的几行数据 写入到新的文件
#mail_contents = list(''.join(sorted(open(result_file), key=lambda s:(int(s.split()[2])))))
sort_contents = list(sorted(open(result_file), key=lambda s:(int(s.split()[2]))))
mail_contents = sort_contents[0:10]
with open(mail_file,'a') as f:
    f.writelines(mail_contents)
