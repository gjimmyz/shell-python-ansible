#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------------
#Author:gong_zheng
#Email:gong_zheng@mingmatechs.com
#FileName:.swap_ckeck.py
#Function:
#Version:1.0
#Created:2021-06-06
#--------------------------------------------------
import psutil

def swap_list():
    swap = psutil.swap_memory()
    swap_total = swap.total
    swap_used = swap.used
    return swap_total,swap_used

res_swap_total,res_swap_used = swap_list()

if res_swap_total != 0 :
    print "swap已开启"
    if res_swap_used != 0 :
        print "swap已开启,并占用swap空间"
    else:
        print "虽然swap已开启,但还没开始使用"
else:
    print "swap没有开启"
