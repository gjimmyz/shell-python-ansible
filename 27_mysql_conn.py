#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.mysql_conn.py
#Function:
#Version:1.0
#Created:2021-07-03
#--------------------------------------------------
import ConfigParser
import os
import MySQLdb
from contextlib import closing

scripts_dir = "/root/scripts/"
mysql_config = 'mysql.config'
config_list_path = os.path.join(scripts_dir,mysql_config)

读取配置文件
config = ConfigParser.ConfigParser()
if os.path.exists(config_list_path):
    with open(config_list_path,'r') as f:
        config.readfp(f)
        host = config.get("client","host")
        user = config.get("client","user")
        passwd = config.get("client","passwd")

初始化mysql连接
def init_conn_mysql():
    mysql_conn = MySQLdb.connect(
        host = host,
        user = user,
        passwd = passwd,
    )
    mysql_conn.autocommit(False)
    return mysql_conn

执行命令
with closing(init_conn_mysql()) as mysql_conn:
    cursor = mysql_conn.cursor()
    cursor.execute('SHOW databases;')
    result = cursor.fetchall()
    print result
