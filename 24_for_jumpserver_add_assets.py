#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:for_jumpserver_add_assets.py
#Function:
#Version:1.0
#Created:2022-11-15
#--------------------------------------------------
# pip install requests drf-httpsig
import requests
import datetime
import json
from httpsig.requests_auth import HTTPSignatureAuth

fmt = '\033[0;3{}m{}\033[0m'.format
class color:
    RED    = 1#红
    GREEN  = 2#绿
    YELLOW = 3#黄

jumpserver_url = 'https://xxxxxxx.mingmatechs.com'
gmt_form = '%a, %d %b %Y %H:%M:%S GMT'

#--------------------------Check SignatureAuth------------------------------
def get_auth(KeyID,SecretID):
    signature_headers = ['(request-target)','accept','date']
    auth = HTTPSignatureAuth(key_id=KeyID,secret=SecretID,algorithm='hmac-sha256',headers=signature_headers)
    return auth

#--------------------------Query Users Info----------------------------------
def get_users_users_info(users_users_info):
    api_url = jumpserver_url + '/api/v1/users/users/'
    params = {
            "username": users_users_info
             }
    res = requests.get(api_url,auth=auth,headers=headers,params=params)
    res_data = json.loads(res.text)
    if res.status_code in [200,201] and res_data:
        print(fmt(color.RED("http_code:%s " % res.status_code)))
        return res_data

#--------------------------Query Assets Nodes Info----------------------------------
def get_assets_nodes_info(assets_nodes_info):
    api_url = jumpserver_url + '/api/v1/assets/nodes/'
    params = {
            "value": assets_nodes_info
             }
    res = requests.get(api_url,auth=auth,headers=headers,params=params)
    res_data = json.loads(res.text)
    if res.status_code in [200,201] and res_data:
        return res_data

#--------------------------Query Assets Ip Info------------------------------
def get_assets_assets_ip_info(assets_assets_ip_info):
    api_url = jumpserver_url + '/api/v1/assets/assets/'
    params = {
            "ip": assets_assets_ip_info
             }
    res = requests.get(api_url,auth=auth,headers=headers,params=params)
    res_data = json.loads(res.text)
    if res.status_code in [200,201] and res_data:
        return res_data

#--------------------------Query Admin Users Info-----------------------------
def get_admin_users_info(admin_users_info):
    api_url = jumpserver_url + '/api/v1/assets/admin-users/'
    params = {
            "name": admin_users_info
             }
    res = requests.get(api_url,auth=auth,headers=headers,params=params)
    res_data = json.loads(res.text)
    if res.status_code in [200,201] and res_data:
        return res_data

#--------------------------Asset Data To Be Filled-----------------------------
def asset_create(assets_assets_ip_info):
    data_to_be_filled = {
        "ip": assets_assets_ip_info,
        "hostname": assets_assets_ip_info,
        "platform": 'Linux',
        "protocol": 'ssh',
        "port": 22,
        "is_active": True,
        "admin_user": admin_id,
        "nodes": [node_id],
        "comment": ""
    }
    api_url = jumpserver_url + '/api/v1/assets/assets/'
    res = requests.post(api_url,auth=auth,headers=headers,data=data_to_be_filled)
    print(fmt(color.RED,(res.headers)))
    print(fmt(color.YELLOW,(res.url)))
    print(fmt(color.GREEN,(res.status_code)))
    res_data = json.loads(res.text)
    if res.status_code in [200,201] and res_data:
        #return res_data
        print(res_data)

def asset_delete(assets_assets_ip_info):
    api_url = jumpserver_url + '/api/v1/assets/assets/'  + f'?ip={assets_assets_ip_info}'
    res = requests.get(api_url,auth=auth,headers=headers)
    asset_id = json.loads(res.text)[0]['id']
    api_url = jumpserver_url + '/api/v1/assets/assets/'  + f'{asset_id}/'
    res = requests.delete(api_url,auth=auth,headers=headers)
    print(fmt(color.RED,('Delete Asset Host Success:%s' % assets_assets_ip_info)))

if __name__ == '__main__':
    KeyID = 'xxxxxx'
    SecretID = 'xxxxxxx'
    auth = get_auth(KeyID,SecretID)
    headers = {
    'Accept': 'application/json',
    #'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Date': datetime.datetime.utcnow().strftime(gmt_form)
    }
    #查询用户信息 暂时没用到这个函数功能
    #users_users_info = "gong_zheng"
    #user_info = get_users_users_info(users_users_info)
    #if user_info:
    #    print(fmt(color.RED,"username:%s\t" % (user_info[0]['username'])))
    #    print("user_name:%s\t" % (user_info[0]['name']))
    #    print("name_id:%s\t" % (user_info[0]['id']))
    #    print("email:%s\t" % (user_info[0]['email']))
    #    print("is_valid:%s\t" % (user_info[0]['is_valid']))
    #    print("is_expired:%s\t" % (user_info[0]['is_expired']))
    #    print("is_active:%s\t" % (user_info[0]['is_active']))
    #    print("total_role_display:%s\t" % (user_info[0]['total_role_display']))

    # 添加资产后会放到 闲置 里
    assets_nodes_info = "闲置"
    node_info = get_assets_nodes_info(assets_nodes_info)
    node_id = node_info[0]['id']

    # linux用户是管理用户 这里用来添加Linux机器
    admin_users_info = "linux用户"
    admin_info = get_admin_users_info(admin_users_info)
    admin_id = admin_info[0]['id']

    assets_assets_ip_info = "10.111.6.163"
    ip_info = get_assets_assets_ip_info(assets_assets_ip_info)
    # 添加资产请开启if else 6行 关闭删除资产5行
    if ip_info:
        print(fmt(color.RED,'ip:%s:已存在' % (ip_info[0]['ip'])))
        print(fmt(color.YELLOW,'id:%s' % (ip_info[0]['id'])))
        print(fmt(color.GREEN,'org_name:%s:' % (ip_info[0]['org_name'])))
    else:
        asset_create(assets_assets_ip_info)

    # 删除资产时请关闭添加资产的6行
    #if ip_info:
    #    assets_id = ip_info[0]['id']
    #    asset_delete(assets_assets_ip_info)
    #else:
    #    print(fmt(color.RED,('该资产不存在:%s' % assets_assets_ip_info)))
