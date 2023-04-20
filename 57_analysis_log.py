57_analysis_log.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
# Author:gong_zheng
# Email:gong_zheng@mingmatechs.com
# FileName:analysis_log.py
# Function:
# Version:1.0
# Created:2023-04-20
#--------------------------------------------------
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

def get_latest_date(log_base_path, ip):
    years = os.listdir(log_base_path)
    years = [year for year in years if os.path.isdir(os.path.join(log_base_path, year))]
    years.sort(reverse=True)
    for year in years:
        months = os.listdir(os.path.join(log_base_path, year))
        months = [month for month in months if os.path.isdir(os.path.join(log_base_path, year, month))]
        months.sort(reverse=True)
        for month in months:
            days = os.listdir(os.path.join(log_base_path, year, month))
            days = [day for day in days if os.path.isdir(os.path.join(log_base_path, year, month, day))]
            days.sort(reverse=True)
            for day in days:
                log_dir = os.path.join(log_base_path, year, month, day, ip)
                if os.path.exists(log_dir):
                    return (year, month, day)

def get_log_files(log_base_path, ip, year, month, day):
    log_dir = f"{log_base_path}/{year}/{month}/{day}/{ip}"
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f == "log" or (f.endswith(".log") and not f.endswith("err.log"))]
    print(f"处理的日志文件：{log_files}")  # 添加调试信息
    return log_files

def analyze_logs(log_files, err_log_file, min_data_points=10):
    hourly_stats = defaultdict(lambda: {"response_time_sum": 0, "total_pings": 0, "lost_pings": 0})
    data_points = 0
    for log_file in log_files:
        print(f"正在处理日志文件：{log_file}")  # 添加日志文件调试信息
        with open(log_file, 'r') as f:
            lines = f.readlines()
            print(f"日志文件 {log_file} 包含 {len(lines)} 行记录")  # 添加记录行数调试信息
            data_points += len(lines)
            for line in lines:
                timestamp, data = line.strip().split(" ", 1)
                hour = int(timestamp.split(":")[0])
                if "ms" in data:
                    response_time = float(data.split(" ")[0])
                    hourly_stats[hour]["response_time_sum"] += response_time
                    hourly_stats[hour]["total_pings"] += 1
                else:
                    hourly_stats[hour]["lost_pings"] += 1
                    hourly_stats[hour]["total_pings"] += 1

    # 处理 err.log 文件
    with open(err_log_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            timestamp = line.strip()
            hour = int(timestamp.split(":")[0])
            hourly_stats[hour]["lost_pings"] += 1
            hourly_stats[hour]["total_pings"] += 1

    print(f"总数据点数：{data_points}")  # 添加总数据点数调试信息

    if data_points < min_data_points:
        return None

    for hour, stats in hourly_stats.items():
        lost_percentage = (stats["lost_pings"] / stats["total_pings"]) * 100
        hourly_stats[hour]["lost_percentage"] = lost_percentage

    return hourly_stats

def generate_report(hourly_stats, report_file_path):
    with open(report_file_path, 'w') as report_file:
        sorted_by_response_time = sorted(hourly_stats.items(), key=lambda x: x[1]["response_time_sum"], reverse=True)
        sorted_by_lost_percentage = sorted(hourly_stats.items(), key=lambda x: x[1]["lost_percentage"], reverse=True)

        report_file.write("5个最差网络时段（按响应时间累加值）：\n")
        for i, (hour, stats) in enumerate(sorted_by_response_time[:5]):
            report_file.write(f"{i + 1}. {hour}:00 - {hour + 1}:00, 响应时间累加值: {stats['response_time_sum']} ms\n")

        report_file.write("\n丢包率排行榜：\n")
        for i, (hour, stats) in enumerate(sorted_by_lost_percentage):
            report_file.write(f"{i + 1}. {hour}:00 - {hour + 1}:00, 丢包率: {stats['lost_percentage']}%\n")

if __name__ == "__main__":
    ip = "157.60.1.2"
    log_base_path = "/root/python3_8_9_project/ping_log"
    report_file_path = "/root/python3_8_9_project/ping_log/report.txt"

    year, month, day = get_latest_date(log_base_path, ip)
    log_files = get_log_files(log_base_path, ip, year, month, day)
    min_data_points = 10
    err_log_file = f"{log_base_path}/{year}/{month}/{day}/{ip}/err.log"
    hourly_stats = analyze_logs(log_files, err_log_file, min_data_points)

    if hourly_stats is not None:
        generate_report(hourly_stats, report_file_path)
    else:
        print(f"没有足够的数据进行分析（至少需要 {min_data_points} 条记录），请稍后再试。")


# 输出
#5个最差网络时段（按响应时间累加值）：
#1. 13:00 - 14:00, 响应时间累加值: 29212.200000000033 ms
#2. 16:00 - 17:00, 响应时间累加值: 28868.600000000042 ms
#3. 15:00 - 16:00, 响应时间累加值: 28799.760000000093 ms
#4. 14:00 - 15:00, 响应时间累加值: 26993.840000000007 ms
#5. 17:00 - 18:00, 响应时间累加值: 16115.53 ms

#丢包率排行榜：
#1. 13:00 - 14:00, 丢包率: 0.20242914979757085%
#2. 17:00 - 18:00, 丢包率: 0.1010611419909045%
#3. 16:00 - 17:00, 丢包率: 0.08542141230068337%
#4. 14:00 - 15:00, 丢包率: 0.05664117813650524%
#5. 15:00 - 16:00, 丢包率: 0.0282326369282891%
#6. 12:00 - 13:00, 丢包率: 0.0%