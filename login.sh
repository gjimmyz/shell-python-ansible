登录第一台机器看看
[root@localhost scripts]# bash login.sh 172.31.67.2
######################################
#        Welcome to aliyun           #
######################################
spawn ssh -p 12345 -q aaa@47.105.42.111
aaa@47.105.42.111's password: 
Last login: Thu Oct 24 10:55:49 2019 from 111.222.333.444

Welcome to Alibaba Cloud Elastic Compute Service !

[aaa@iZm5e6evv00x6vs4ibppiyZ ~]$ su -
Password: 
Last login: Thu Oct 24 10:55:49 CST 2019 on pts/0
root@172.31.67.2:~# exit
logout
[aaa@iZm5e6evv00x6vs4ibppiyZ ~]$ exit
logout

登录第二台机器看看
[root@localhost scripts]# bash login.sh 172.31.67.3
######################################
#        Welcome to aliyun           #
######################################
spawn ssh -p 12345 -q aaa@47.104.102.222
aaa@47.104.102.222's password: 
Last login: Thu Oct 24 10:55:44 2019 from 111.222.333.444

Welcome to Alibaba Cloud Elastic Compute Service !

[aaa@iZm5e6evv00x6vs4ibppiuZ ~]$ su -
Password: 
Last login: Thu Oct 24 10:55:44 CST 2019 on pts/0
root@172.31.67.3:~# exit
logout
[aaa@iZm5e6evv00x6vs4ibppiuZ ~]$ exit
logout
[root@localhost scripts]# 

相关配置文件
n_ip=172.31.67.2 ssh_w_ip=47.105.42.111 ssh_user=aaa ssh_pass=123456 ssh_port=12345
n_ip=172.31.67.3 ssh_w_ip=47.104.102.222 ssh_user=aaa ssh_pass=654321 ssh_port=12345

相关脚本
[root@localhost scripts]# cat login.sh 
#!/bin/bash
#--------------------------------------------------
#Author:gjimmyz(gongzheng)
#Email:85646830@qq.com
#FileName:login.sh
#Function: 
#Version:1.0 
#Created:2019-10-24
#--------------------------------------------------
#安装expect
#yum -y install expect
#============================相关配置文件示例_配置文件路径/root/scripts/ipip.conf=========================================
#内网IP           外网UP                  用户                     密码                                      端口
#n_ip=172.31.67.2 ssh_w_ip=47.105.42.111  ssh_user=aaa ssh_pass=123456 ssh_port=12345
#n_ip=172.31.67.3 ssh_w_ip=47.104.102.222 ssh_user=aaa ssh_pass=654321 ssh_port=12345
#============================配置文件文件示例结束==========================================================================
#传递一个IP参数
xargs_ip="$1"
#这个是root密码 登录上去后 切换到root用户
r_pass="123456789"
#配置文件路径
pz_file="/root/scripts/ipip.conf"
#具体用法
#bash login.sh 172.31.67.2

function action ()
{
    wcnum=$(cat ${pz_file}|wc -l)
    for ((k=1;k<=${wcnum};k++))
    do
        n_w_ip=`cat ${pz_file}|sed -n "$k"p|awk '{print $1}'|awk -F'=' '{print $2}'`
        s_w_ip=`cat ${pz_file}|sed -n "$k"p|awk '{print $2}'|awk -F'=' '{print $2}'`
        s_user=`cat ${pz_file}|sed -n "$k"p|awk '{print $3}'|awk -F'=' '{print $2}'`
        s_pass=`cat ${pz_file}|sed -n "$k"p|awk '{print $4}'|awk -F'=' '{print $2}'`
        s_port=`cat ${pz_file}|sed -n "$k"p|awk '{print $5}'|awk -F'=' '{print $2}'`
        for ip in $n_w_ip
        do
            if [[ ${xargs_ip} != ${ip} ]]
            then
               break
               #continue
            fi
            printf "\033[32m######################################\033[0m\n"
            printf "\033[32m#        Welcome to aliyun           #\033[0m\n"
            printf "\033[32m######################################\033[0m\n"
            expect -c"
            spawn ssh -p ${s_port} -q ${s_user}@${s_w_ip}
            expect {
            \"yes/no\" {send \"yes\r\";exp_continue}
            \"assword:\" {send \"${s_pass}\r\"}
            }
            expect \"\$*\"
            send \"su -\n\"
            expect \"assword:\"
            send \"$r_pass\n\"
            interact"
        done
    done
}
action
