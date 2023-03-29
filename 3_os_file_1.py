#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gongzheng
#Email:85646830@qq.com
#FileName:os_file_1.py
#Function: 
#Version:1.0 
#Created:2020-04-20
#--------------------------------------------------
import os

f_file="/root/scripts/test.txt"
f_content="""
送杜少府之任蜀州
城阙辅三秦，风烟望五津。
与君离别意，同是宦游人。
海内存知己，天涯若比邻。
无为在歧路，儿女共沾巾。
"""

#判断是否存在文件
if (os.path.isfile(f_file)):
    print "该文件已存在"
else:
    #写入内容到文件里
    with open(f_file,'w') as f:
	#去除头部空行
        f.write(f_content.lstrip())
    #读取文件
    with open(f_file,'r') as f:
	#循环读取 直到全部读取完
        while True:
	    line=f.readline()
	    if len(line) == 0:
	        break
	    #strip去除空行
	    print line.strip()

效果:		
[root@localhost scripts]# python os_file_1.py
送杜少府之任蜀州
城阙辅三秦，风烟望五津。
与君离别意，同是宦游人。
海内存知己，天涯若比邻。
无为在歧路，儿女共沾巾。
