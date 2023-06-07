#!/bin/bash
#--------------------------------------------------
#Author:gongzheng
#Email:gong_zheng@mingmatechs.com
#FileName:md5sum_check_file.sh
#Function:
#Version:1.0
#Created:2023-06-07
#--------------------------------------------------
set -o nounset
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=$PATH:/usr/local/bin:/usr/bin:/usr/sbin

# 定义要计算的目录
target_directory="/home/seq/Huada_Jingzhou/upload/workspace/E100074248/L01/calFile/"
# 定义保存结果的文件
output_file="/root/scripts/md5sum_20230607"
# 开始时间
start=$(date "+%s")
# 初始化计数器
count=0
# 计算目录下所有文件的md5值
for file in ${target_directory}*
do
    # 使用md5sum计算文件的md5值并将结果追加到输出文件中
    md5sum $file >> $output_file &
    # 计数器加1
    ((count++))
    # 如果当前已有10个进程在计算md5值，那么等待这10个进程全部完成后再继续
    if [[ $((count%10)) -eq 0 ]]; then
        wait
    fi
done
# 等待所有后台进程完成
wait
# 结束时间
end=$(date "+%s")
# 输出计算所需的时间
echo "time: $(expr $end - $start)" >> $output_file