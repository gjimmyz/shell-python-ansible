直接上代码
[root@localhost scripts]# cat file_1.sh
#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:85646830@qq.com
#FileName:file_1.sh
#Function: 
#Version:1.0 
#Created:2020-04-20
#--------------------------------------------------
set -o nounset
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin

#/root/scripts/ 已存在 不存在请自行新建目录
f_file="/root/scripts/test.txt"
f_content='
送杜少府之任蜀州
城阙辅三秦，风烟望五津。
与君离别意，同是宦游人。
海内存知己，天涯若比邻。
无为在歧路，儿女共沾巾。
'
echo_warn="该文件已存在"

if [[ -e ${f_file} ]]
then
    echo ${echo_warn}
else
    echo ${f_content} > ${f_file} 	
    if [[ -n ${f_file} ]]
    then
        for i in $(cat ${f_file})
	do
	    echo $i    
	done
    fi
fi

效果:
[root@localhost scripts]# sh file_1.sh
送杜少府之任蜀州
城阙辅三秦，风烟望五津。
与君离别意，同是宦游人。
海内存知己，天涯若比邻。
无为在歧路，儿女共沾巾。

PS:
有相应的python代码 主要是为了和python比较下
具体地址:https://github.com/gjimmyz/python/blob/master/file_1.py
