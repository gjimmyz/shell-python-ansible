53_proemethus_api_level_1.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:promethues_api_level_1.py
#Function:
#Version:1.0
#Created:2023-04-07
#--------------------------------------------------
import os
import time
from datetime import datetime
import requests

def prometheus_request(url, query):
    try:
        response = requests.get(url + 'query', params={'query': query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("请求错误：", e)
        return None

def process_result(result):
    if result and result.get('data', {}).get('result'):
        return float(result['data']['result'][0]['value'][1])
    else:
        print("没有数据")
        return None

def write_log(path, value):
    with open(path, 'a') as f:
        f.write(f"{value} {datetime.now().strftime('%H:%M')}\n")

def main():
    base_path = "/root/scripts/python3_8_9_project/promethues_api_log/"
    ip = "10.xxx.xxx.75"
    prometheus_url = "http://10.xxx.xxx.76:9090/api/v1/"

    while True:
        current_time = datetime.now()
        current_date = current_time.strftime("%Y/%m/%d/")
        log_path = f"{base_path}{current_date}{ip}/"

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if current_time.minute % 15 == 0:
            query_15m = 'avg(node_load15{{instance="{0} node_exporter"}}) / count(count(node_cpu_seconds_total{{instance="{0} node_exporter"}}) by (cpu)) * 100'.format(ip)
            result_15m = prometheus_request(prometheus_url, query_15m)
            value_15m = process_result(result_15m)
            if value_15m is not None:
                write_log(f"{log_path}15.log", value_15m)

        if current_time.minute % 5 == 0:
            query_5m = 'avg(node_load5{{instance="{0} node_exporter"}}) / count(count(node_cpu_seconds_total{{instance="{0} node_exporter"}}) by (cpu)) * 100'.format(ip)
            result_5m = prometheus_request(prometheus_url, query_5m)
            value_5m = process_result(result_5m)
            if value_5m is not None:
                write_log(f"{log_path}5.log", value_5m)

        query_1m = '(sum by(instance) (irate(node_cpu_seconds_total{{instance="{0} node_exporter", mode!="idle"}}[1m])) / on(instance) group_left sum by(instance)((irate(node_cpu_seconds_total{{instance="{0} node_exporter"}}[1m])))) * 100'.format(ip)
        result_1m = prometheus_request(prometheus_url, query_1m)
        value_1m = process_result(result_1m)
        if value_1m is not None:
            write_log(f"{log_path}1.log", value_1m)

        time.sleep(60)

if __name__ == "__main__":
    main()