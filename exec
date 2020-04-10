exec这个命令通常用的比较少 但还是要了解下哈
1)调用并执行指定的命令
重置root密码的会用到
exec /sbin/init
这个时候再执行init的时候什么不需要加参数呢 因为是执行/sbin/init的本身程序 程序还没起来。。哪里来init命令呢。

2)重定向     一般用在shell里
exec 1>$logfile
exec 2>$logfile

3)可以和find结合使用
find . -type f -exec ls -l {} \;

目前就见过这三个场景
