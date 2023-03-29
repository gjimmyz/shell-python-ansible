#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:create_qemu.py
#Function:
#Version:1.0#Created:2022-12-10
#--------------------------------------------------
#need jq cmd
import subprocess
import time
import sys
import random

fmt = '\033[0;3{}m{}\033[0m'.format
class color:
    RED    = 1#红
    GREEN  = 2#绿
    YELLOW = 3#黄

def get_pve_nodes():
    get_pve_nodes_cmdline = "pvesh get /nodes  --output-format json-pretty"
    get_pve_nodes_jq_cmdline = (get_pve_nodes_cmdline + "|" + "jq" + " --raw-output " + "'" +".[]" + "|" + '"' + '\\' + "(" + ".[" '"status"' "]" + ")" + "," + '\\' + "(" + ".[" '"node"' "]" + ")" + "," + '\\' + "(" + ".[" '"mem"' "]" + ")" + "," + '\\' + "(" + ".[" '"cpu"' "]" + ")" + '"' + "'")
    #print(fmt(color.YELLOW,("Get Pve Node Status Cmdline Is: %s" % get_pve_nodes_jq_cmdline)))
    stdout_data = subprocess.getoutput(get_pve_nodes_jq_cmdline)
    return(stdout_data)
    #print(stdout_data)

def get_pve_real_nodes():
    all_nodes = get_pve_nodes()
    node_of_list = list(i.split(',') for i in (all_nodes.split('\n')) )
    #print(node_of_list)
    sort_res = sorted(node_of_list,key=lambda x:(x[2],x[3]))
    sort_first_node = (sort_res[0])
    real_node_name = sort_first_node[1]
    #print(fmt(color.YELLOW,("Get Pve Real Node Is: %s" % real_node_name)))
    return(real_node_name)

def get_vmid_range(vmid_begin,vmid_end):
    vmid_num_range = []
    for i in range(vmid_begin,vmid_end):
        vmid_num_range.append(i)
    return(vmid_num_range)
    #print(vmid_num_range)

def get_cluster_resources_vmid():
    get_pve_vmid_cmdline = "pvesh get /cluster/resources --output-format json-pretty --type vm"
    get_pve_vmid_jq_cmdline = (get_pve_vmid_cmdline + "|" + "jq" + " --raw-output " + "'" +".[]" + "|" + '"' + '\\' + "(" + ".[" '"vmid"' "]" + ")" + '"' + "'")
    #print(fmt(color.YELLOW,("Get Cluster Resource Vmid Cmdline Is: %s" % get_pve_vmid_jq_cmdline)))
    stdout_data = subprocess.getoutput(get_pve_vmid_jq_cmdline)
    return(stdout_data)
    #print(stdout_data)

def get_pve_real_vmid():
    vmid_num_list = get_vmid_range(vmid_begin,vmid_end)
    #print(vmid_num_list)
    real_vmid_str = get_cluster_resources_vmid()
    real_vmid_int = list(map(int,real_vmid_str.split()))
    #print(real_vmid_int)
    set1 = set(vmid_num_list)
    set2 = set(real_vmid_int)
    set1_and_set2_intersection_list = (list(set1 & set2))
    if set1_and_set2_intersection_list:
        #print(set1_and_set2_intersection_list)
        final_different_list = sorted(list(set(set1).difference(set(set1_and_set2_intersection_list))))
        return(final_different_list[0])
        #print(final_different_list[0])
        #print(type(final_different_list[0]))
    else:
        return(vmid_num_list[0])

def print_wait(s_str):
    for i in s_str + '\n':
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(random.random() * 0.5)
        #time.sleep(random.random() * 1)

def check_pve_node_qemu_status():
    check_pve_node_qemu_status_cmdline = ("pvesh " + "get " + "/nodes/" + real_pve_node + "/qemu/" + real_pve_vmid_str + "/status" )
    #print(fmt(color.YELLOW,("Check Pve Node Qemu Status Cmdline Is: %s" % check_pve_node_qemu_status_cmdline)))
    stdout_data = subprocess.getoutput(check_pve_node_qemu_status_cmdline)
    return(stdout_data)
    #print(stdout_data)

def update_pve_node_qemu_vlan_tags():
    """
    tag=2273 根据情况修改
    """
    update_pve_node_qemu_vlan_tags_cmdline = ("pvesh " + "set " + "/nodes/" + real_pve_node + "/qemu/" + real_pve_vmid_str + "/config " + "--net0 " + "virtio" +"," + "bridge=vmbr1" + "," + "firewall=1" + "," + "tag=2273")
    #print(fmt(color.YELLOW,("Update Pve Node Qemu Vlan Cmdline Is: %s" % update_pve_node_qemu_vlan_tags_cmdline)))
    stdout_data = subprocess.getoutput(update_pve_node_qemu_vlan_tags_cmdline)
    return(stdout_data)
    #print(stdout_data)

def create_pve_node_qemu_ipconfig():
    """
    gw=xxx 和tags对应 根据情况修改
    """
    create_pve_node_qemu_ipconfig_cmdline = ("pvesh " + "create " + "/nodes/" + real_pve_node + "/qemu/" + real_pve_vmid_str + "/config " + "--ipconfig0 " + "ip=10.21.254.51" + "/24" + "," + "gw=10.21.254.254")
    #print(fmt(color.YELLOW,("Update Pve Node Qemu Ipconfig Cmdline Is: %s" % create_pve_node_qemu_ipconfig_cmdline)))
    stdout_data = subprocess.getoutput(create_pve_node_qemu_ipconfig_cmdline)
    return(stdout_data)
    #print(stdout_data)

def create_pve_node_qemu_start():
    create_pve_node_qemu_start_cmdline = ("pvesh " + "create " + "/nodes/" + real_pve_node + "/qemu/" + real_pve_vmid_str + "/status" + "/start")
    #print(fmt(color.YELLOW,("Create Pve Node Qemu Start Cmdline Is: %s" % create_pve_node_qemu_start_cmdline)))
    stdout_data = subprocess.getoutput(create_pve_node_qemu_start_cmdline)
    return(stdout_data)

def check_pve_node_qemu_status_current():
    check_pve_node_qemu_status_current_cmdline = ("pvesh " + "get " + "/nodes/" + real_pve_node + "/qemu/" + real_pve_vmid_str + "/status" + "/current")
    #print(fmt(color.YELLOW,("Check Pve Node Qemu Status Current Cmdline Is: %s" % check_pve_node_qemu_status_current_cmdline)))
    stdout_data = subprocess.getoutput(check_pve_node_qemu_status_current_cmdline)
    return(stdout_data)

if __name__=="__main__":
    """
    vmid:
    100-199都放test for lxc and qemu
    7000-7999都放prod for lxc
    8000-8999都放prod for qemu
    99xx-9999都放prod for template
    """
    vmid_begin = 130
    vmid_end = 140
    real_pve_vmid_int = get_pve_real_vmid()
    real_pve_vmid_str = str(real_pve_vmid_int)
    real_pve_node = get_pve_real_nodes()
    #print(type(real_pve_vmid_str))
    #print(real_pve_vmid_str)
    #print(type(real_pve_node))
    #print(real_pve_node)
    """
    template:proxmox-node05
    vm:qemu
    vmid:9997
    pool:devops-user-pools
    storage:rbd_hdd
    clone:full
    """
    cmdline_for_qemu = ("pvesh " + "create " + "/nodes" + "/proxmox-node05" + "/qemu" + "/9997" + "/clone " + "--newid " + real_pve_vmid_str + " " + "--full " +"1 " + "--name " + "please-change-me " + "--target " + real_pve_node + " " + "--pool " + "devops-user-pools " + "--storage " + "rbd_hdd")
    #print(fmt(color.YELLOW,("Create Qemu Cmdline Is: %s" % cmdline_for_qemu)))
    #stdout_data = subprocess.run(cmdline_for_qemu,shell=True,stdout=subprocess.PIPE)
    stdout_data = subprocess.Popen(
            cmdline_for_qemu,
            stdout=subprocess.PIPE,
            shell=True
            )
    begin_time = time.time()
    while 1:
        process_run = subprocess.Popen.poll(stdout_data)
        if process_run is None:
            #print_wait('1、正在创建虚拟机中，请耐心等待，请勿暂停中断本程序，如有异常请联系作者本人。')
            print_wait('1、Proxmox私有云平台目前正在处理创建云服务器的请求，请耐心等待，会���费30秒时间，如有异常请联系龚崝或mail to gong_zheng@mingmatechs.com。')
            time.sleep(1)
        else:
            #print(fmt(color.YELLOW,('Create Qemu Ok')))
            break
    #end_time = time.time()
    #time_used = str(round(end_time - begin_time))
    #print(fmt(color.GREEN,("创建虚拟机共花费了: %ss" % time_used)))
    modify_vlan_ip_start_ShowRunningStatus = check_pve_node_qemu_status()
    if modify_vlan_ip_start_ShowRunningStatus:
        print_wait('2、云服务器创建好了，接下来修改配置。')
        update_pve_node_qemu_vlan_tags()
        print_wait('3、vlan配置好了。')
        set_ip = create_pve_node_qemu_ipconfig()
        if set_ip:
            print_wait('4、ip配置好了。')
        qemu_start = create_pve_node_qemu_start()
        if qemu_start:
            print_wait('5、云服务器已开机。')
        show_running_status = check_pve_node_qemu_status_current()
        if show_running_status:
            print_wait('6、云服务器信息如下。')
            print(show_running_status)
            end_time = time.time()
            time_used = str(round(end_time - begin_time))
            print(fmt(color.GREEN,("创建虚拟机共花费了: %ss" % time_used)))
    else:
        pass
