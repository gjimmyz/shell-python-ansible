#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.ftp_client.py
#Function:
#Version:1.0
#Created:2021-06-14
#--------------------------------------------------
import socket
import os
import ftplib

ftp_server_ip = "10.81.112.86"
ftp_server_port = 2121
ftp_username = 'user'
ftp_passwd = '12345'
ftp_timeout = 10
ftp_cmd = 'RETR '
ftp_download_path = '/root/scripts/rsync_log_bak'

#使用socket检查连接情况
def action(ftp_server_ip,ftp_server_port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return_num = s.connect_ex((ftp_server_ip,ftp_server_port))
    if return_num == 0:
        print "ftp_ip:%s连接正常,ftp_port:%d端口已开放" % (ftp_server_ip,ftp_server_port)
        return return_num
    else:
        print "ftp_ip:%s连接失败或ftp_port:%d端口没开放" % (ftp_server_ip,ftp_server_port)
    s.close()

#ftp建立链接后下载
if action(ftp_server_ip,ftp_server_port) == 0:
    ftp_conn = ftplib.FTP()
    ftp_conn.set_debuglevel(2)
    ftp_conn.connect(ftp_server_ip,ftp_server_port,ftp_timeout)
    ftp_conn.login(ftp_username,ftp_passwd)
    #登陆上去后的目录是/root/scripts 需要下载的文件在/root/scripts/rsync_log/目录里
    ftp_conn.cwd('rsync_log')
    #返回需要下载的文件列表
    list_all = ftp_conn.nlst()

    for f_list in list_all:
        path_exists = os.path.exists(ftp_download_path)
        if not path_exists:
            os.makedirs(ftp_download_path)
        file_dest_path = os.path.join(ftp_download_path,f_list)
        try:
            with open(file_dest_path,'wb') as f:
                ftp_conn.retrbinary(ftp_cmd + f_list,f.write)
        except ftplib.error_perm:
            pass
    ftp_conn.set_debuglevel(0)
    ftp_conn.quit()
