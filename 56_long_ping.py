56_long_ping.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Author:gong_zheng
# Email:gong_zheng@mingmatechs.com
# FileName:long_ping.py
# Function:
# Version:1.0
# Created:2023-04-20
#--------------------------------------------------
import os
import time
import subprocess
from datetime import datetime, timedelta

def create_dir(directory):
    if not os.path.exists(directory):        os.makedirs(directory)
def ping(ip):
    result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def parse_ping_result(output):
    if "1 packets transmitted, 1 received" in output:
        response_time = float(output.split("time=")[1].split(" ms")[0])
        return response_time, False
    else:
        error_message = output.split('\n')[-2]
        return error_message, True

def write_log(log_path, content):
    with open(log_path, 'a') as log_file:
        log_file.write(content + "\n")

def ping_loop(ip):
    while True:
        current_time = datetime.now()
        year, month, day = current_time.strftime("%Y"), current_time.strftime("%m"), current_time.strftime("%d")
        hour, minute, second = current_time.strftime("%H"), current_time.strftime("%M"), current_time.strftime("%S")
        timestamp = f"{hour}:{minute}:{second}"

        log_base_path = "/root/python3_8_9_project/ping_log"
        log_dir = f"{log_base_path}/{year}/{month}/{day}/{ip}"
        create_dir(log_dir)

        log_path = f"{log_dir}/log"
        err_path = f"{log_dir}/err.log"

        for _ in range(3):
            result = ping(ip)
            response, is_error = parse_ping_result(result.stdout)

            if not is_error:
                write_log(log_path, f"{timestamp} {response} ms")
                break
            else:
                write_log(err_path, f"{timestamp} {response}")
                time.sleep(5)
        time.sleep(1)

if __name__ == "__main__":
    ip = "xxx.xxx.xxx.xxx"
    ping_loop(ip)

# 相关结构
#tree ping_log/
#ping_log/
#├── 2023
#│   └── 04
#│       └── 20
#│           └── xxx.xxx.xxx.xxx
#│               ├── err.log
#│               └── log
#└── report.txt
#
#4 directories, 3 files
