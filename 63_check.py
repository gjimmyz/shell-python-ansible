#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:check.py
#Function:
#Version:1.0
#Created:2023-07-06
#--------------------------------------------------
import os
import time
import datetime
import subprocess

# Constants
DIRECTORY = "/root/scripts/check_system_stress"
SLEEP_TIME = 1800
NETWORK_DEVICE = 'ens2f1'

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_largest_mount():
    df_output = subprocess.check_output(['df', '-Th']).decode('utf-8').split('\n')
    mount_lines = df_output[1:-1]
    def sort_key(line):
        try:
            size = float(line.split()[2][:-1])
            unit = line.split()[2][-1]
            if unit == 'T':
                size = size * 1024            return size
        except ValueError:
            return 0
    mount_lines.sort(key=sort_key, reverse=True)
    largest_mount_device = mount_lines[0].split()[0]
    return largest_mount_device

def write_to_file(content):
    date_today = datetime.datetime.now()
    directory = f"{DIRECTORY}/{date_today.year}/{date_today.month}/{date_today.day}"
    create_directory_if_not_exists(directory)
    file_path = os.path.join(directory, "system_usage.txt")
    with open(file_path, 'a') as f:
        f.write(content)

def get_network_data(device):
    output = os.popen(f'ip -s link show {device}').read().split('\n')
    rx_bytes = int(output[3].split()[0])
    tx_bytes = int(output[5].split()[0])
    return rx_bytes, tx_bytes

def get_disk_write_sectors(device):
    with open(f"/sys/block/{device}/stat") as f:
        return int(f.read().split()[6])

# Set the disk device to the largest mounted device
DISK_DEVICE = get_largest_mount().split("/")[-1]  # Remove "/dev/" prefix
# Removing partition number from the device name (sda1 -> sda)
DISK_DEVICE = ''.join([i for i in DISK_DEVICE if not i.isdigit()])
print(f"Monitoring Disk Device: {DISK_DEVICE}")

last_net_data = get_network_data(NETWORK_DEVICE)
last_disk_write_sectors = get_disk_write_sectors(DISK_DEVICE)

while True:
    time.sleep(SLEEP_TIME)
    # Get current date and time
    now = datetime.datetime.now()
    # Get CPU usage
    cpu_usage = os.popen('vmstat 1 2').readlines()[-1].split()[12]
    # Get network send and received data
    current_net_data = get_network_data(NETWORK_DEVICE)
    net_sent = (current_net_data[1] - last_net_data[1]) / (1024 * 1024 * 1024)  # convert bytes to GB
    net_recv = (current_net_data[0] - last_net_data[0]) / (1024 * 1024 * 1024)  # convert bytes to GB
    last_net_data = current_net_data
    # Get disk write data
    current_disk_write_sectors = get_disk_write_sectors(DISK_DEVICE)
    hourly_disk_write = (current_disk_write_sectors - last_disk_write_sectors) * 512 / (1024 * 1024 * 1024)  # convert sectors to GB
    last_disk_write_sectors = current_disk_write_sectors
    # Write the result to the file
    write_to_file(f"{now.strftime('%Y-%m-%d %H:%M:%S')} CPU Usage: {cpu_usage}% Network Sent: {round(net_sent, 1)}GB Network Recv: {round(net_recv, 1)}GB HourlyDisk Write: {round(hourly_disk_write, 1)}GB\n")