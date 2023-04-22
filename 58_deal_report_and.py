58_deal_report_and_monitor_process.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Author:gong_zheng
# Email:gong_zheng@mingmatechs.com
# FileName:deal_report_and_monitor_process.py
# Function:
# Version:1.0
# Created:2023-04-20
#--------------------------------------------------
import os
import shutil
from datetime import datetime

# 定义文件路径
report_file_path = "/root/python3_8_9_project/ping_log/report.txt"
dir_base_path = "/root/python3_8_9_project/ping_log/report_"

# 获取当前时间
now = datetime.now()
year = now.year
month = now.month
day = now.day

# 创建目录
current_dir = f"{dir_base_path}{year}/{month}/{day}/"
os.makedirs(current_dir, exist_ok=True)

# 检查文件是否存在且不为空
if os.path.exists(report_file_path) and os.path.getsize(report_file_path) > 0:
    # 复制文件
    shutil.copy(report_file_path, current_dir)

    # 清空文件内容
    with open(report_file_path, 'w') as file:
        file.write("")

# 检查 long_ping.py 进程
result = os.popen("ps -ef|grep -v grep|grep long_ping.py|wc -l").read().strip()
count = int(result)

if count == 1:
    os.system("pkill -f long_ping.py")
elif count == 0:
    os.system("source /root/python3_8_9_project/bin/activate && python /root/python3_8_9_project/long_ping.py")

#设置了计划任务