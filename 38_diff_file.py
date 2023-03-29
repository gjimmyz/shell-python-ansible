#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.diff_file.py
#Function:
#Version:1.0
#Created:2021-05-27
#--------------------------------------------------
import os
import difflib
import sys

difffile1 = "/root/scripts/mail_send"
difffile2 = "/root/scripts/mail_send1"

#要求填写2个参数 也就是2个文件名
try:
    diff_file1 = sys.argv[1]
    diff_file2 = sys.argv[2]
except Exception as e:
    print("Error:" + str(e))
    print("Usage: xxx.py filename1 filename2")
    sys.exit()

diff_path = "/root/scripts/diff_log/"
#如果目录不存在 就创建目录
path_exists = os.path.exists(diff_path)
if not path_exists:
    os.makedirs(diff_path)

if os.path.exists(difffile1):
    with open(difffile1,'r') as f:
        while True:
            line_1 = f.readline()
            if len(line_1) == 0:
                break
            contents_1 = line_1.strip()

if os.path.exists(difffile2):
    with open(difffile2,'r') as f:
        while True:
            line_2 = f.readline()
            if len(line_2) == 0:
                break
            contents_2 = line_2.strip()

for i in difflib.context_diff(contents_1.splitlines(),contents_2.splitlines(),fromfile=difffile1,tofile=difffile2):
    print i.strip()
