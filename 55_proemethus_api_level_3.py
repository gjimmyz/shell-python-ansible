55_proemethus_api_level_3.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:promethues_api_level_3.py
#Function:
#Version:1.0
#Created:2023-04-07
#--------------------------------------------------
import osimport time
import requests
from datetime import datetime
import configparser

def read_config(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)    return config

def read_iplist(iplist_file_path):
    with open(iplist_file_path) as f:
        ip_list = [line.strip() for line in f.readlines()]
    return ip_list
def request_prometheus(prometheus_url, query):
    try:
        response = requests.get(f'{prometheus_url}query', params={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常: {e}")
        return None

def process_result(result):
    if result and 'data' in result and 'result' in result['data']:
        value = result['data']['result'][0]['value'][1]
        return round(float(value), 2)
    else:
        return None

def save_log(log_path, ip, cpu_usage, timestamp):
    with open(log_path, 'a') as f:
        f.write(f"{ip} {cpu_usage} {timestamp}\n")

def main():
    config = read_config('/root/scripts/python3_8_9_project/config.txt')
    prometheus_url = config.get('General', 'prometheus_url')
    iplist_file = config.get('General', 'iplist_file')
    ip_list = read_iplist(iplist_file)

    while True:
        now = datetime.now()
        current_year = now.strftime('%Y')
        current_month = now.strftime('%m')
        current_day = now.strftime('%Y%m%d')
        current_timestamp = now.isoformat()[:-7]

        for ip in ip_list:
            base_log_path = f"/root/scripts/python3_8_9_project/promethues_api_log/{current_year}/{current_month}/{current_day}/{ip}/cpu"

            query_1min = config.get('Queries', 'query_1min').format(ip)
            query_5min = config.get('Queries', 'query_5min').format(ip)
            query_15min = config.get('Queries', 'query_15min').format(ip)

            if now.minute % 15 == 0:
                query = query_15min
                log_path = f"{base_log_path}/15.log"
            elif now.minute % 5 == 0:
                query = query_5min
                log_path = f"{base_log_path}/5.log"
            else:
                query = query_1min
                log_path = f"{base_log_path}/1.log"

            os.makedirs(os.path.dirname(log_path), exist_ok=True)

            result = request_prometheus(prometheus_url, query)
            cpu_usage = process_result(result)
            if cpu_usage is not None:
                save_log(log_path, ip, cpu_usage, current_timestamp)
                print(f"{ip} {cpu_usage} {current_timestamp}")

        time.sleep(60)

if __name__ == '__main__':
    main()

# 配置文件
cat iplist
10.xxx.xxx.84
10.xxx.xxx.75

# 配置文件
cat config.txt
[General]
prometheus_url=http://10.xxx.xxx.76:9090/api/v1/
iplist_file=/root/scripts/python3_8_9_project/iplist

[Queries]
query_1min=(sum by(instance) (irate(node_cpu_seconds_total{{instance="{0} node_exporter", mode!="idle"}}[1m])) / on(instance) group_left sum by(instance)((irate(node_cpu_seconds_total{{instance="{0} node_exporter"}}[1m])))) * 100
query_5min=avg(node_load5{{instance="{0} node_exporter"}}) / count(count(node_cpu_seconds_total{{instance="{0} node_exporter"}}) by (cpu)) * 100
query_15min=avg(node_load15{{instance="{0} node_exporter"}}) / count(count(node_cpu_seconds_total{{instance="{0} node_exporter"}}) by (cpu)) * 100
[root@ceph03_node16 python3_8_9_project]#