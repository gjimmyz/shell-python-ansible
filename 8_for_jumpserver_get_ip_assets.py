#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:for_jumpserver_get_ip_assets.py
#Function:
#Version:1.0
#Created:2023-03-28
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

jumpserver_url = 'https://xxxxx.mingmatechs.com'
gmt_form = '%a, %d %b %Y %H:%M:%S GMT'

#--------------------------Check SignatureAuth------------------------------
def get_auth(KeyID,SecretID):
    signature_headers = ['(request-target)','accept','date']
    auth = HTTPSignatureAuth(key_id=KeyID,secret=SecretID,algorithm='hmac-sha256',headers=signature_headers)
    return auth
#--------------------------Query Assets Ip Info------------------------------
def get_assets_assets_ip_info():
    api_url = jumpserver_url + '/api/v1/assets/assets/'
    res = requests.get(api_url,auth=auth,headers=headers)
    res_data = json.loads(res.text)
    return res_data

if __name__ == '__main__':
    KeyID = 'xxxxxxxxxxxx'
    SecretID = 'xxxxxxxx'
    auth = get_auth(KeyID,SecretID)
    headers = {
    'Accept': 'application/json',
    #'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
    'Date': datetime.datetime.utcnow().strftime(gmt_form)
    }
    ip_info = get_assets_assets_ip_info()
    if ip_info:
        for item in ip_info:
        #print(item['ip'])
            print(fmt(color.GREEN,'%s' % (item['ip'])))
