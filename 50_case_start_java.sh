50_case_start_java.sh

#!/bin/bash

# 定义Jar包路径和PID文件路径
JAR_PATH=/root/my-test/target/demo4-0.0.1-SNAPSHOT.jar
PID_FILE=./pid.txt

# 定义启动命令和停止命令
START_CMD="java -jar $JAR_PATH > /dev/null & echo \$! > $PID_FILE"
STOP_CMD="kill \$(cat $PID_FILE)"

# 处理命令行参数
case "$1" in
    start)
        # 启动应用程序
        if [ -f "$PID_FILE" ]; then
            echo "服务已经在运行中！"
            exit 1
        fi

        eval $START_CMD
        echo "服务已经成功启动！"
        ;;

    stop)
        # 停止应用程序
        if [ ! -f "$PID_FILE" ]; then
            echo "服务已经停止！"
            exit 0
        fi

        # 尝试使用SIGTERM信号停止Java进程
        kill $(cat $PID_FILE)
        for i in {1..10}; do
            if ps -p $(cat $PID_FILE) > /dev/null; then
                sleep 1
            else
                break
            fi
        done

        # 如果优雅方式失败，再使用SIGKILL信号强制终止
        if ps -p $(cat $PID_FILE) > /dev/null; then
            eval $STOP_CMD
            echo "服务已经被强制终止！"
        else
            rm $PID_FILE
            echo "服务已经成功停止！"
        fi
        ;;

    restart)
        # 重新部署应用程序
        if [ -f "$PID_FILE" ]; then
            eval $STOP_CMD
        fi

        eval $START_CMD
        echo "服务已经成功部署！"
        ;;

    *)
        # 如果命令不匹配，则显示帮助信息
        echo "用法：$0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0