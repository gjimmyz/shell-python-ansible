cat mysql.config
[client]
host = localhost
user = root
passwd = 123456

#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.mysql_conn_config.py
#Function:
#Version:1.0
#Created:2021-07-02
#--------------------------------------------------
import ConfigParser
import os

scripts_dir = "/root/scripts/"
mysql_config = 'mysql.config'
config_list_path = os.path.join(scripts_dir,mysql_config)

读取配置
config = ConfigParser.ConfigParser()
if os.path.exists(config_list_path):
    with open(config_list_path,'r') as f:
        config.readfp(f)
        host = config.get("client","host")
        user = config.get("client","user")
        passwd = config.get("client","passwd")
        print host
        print user
        print passwd
