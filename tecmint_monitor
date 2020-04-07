1、fork https://github.com/atarallo/TECMINT_MONITOR
2、fork https://www.shiyanlou.com/courses/597/learning(Shell脚本实现Linux系统监控)

PS:以下改了二处地方
#! /bin/bash
# unset any variable which system may be using
# clear the screen


while getopts ivh name
do
        case $name in
          i)iopt=1;;
          v)vopt=1;;
          h)hopt=1;;
         *)echo "Invalid arg";;
        esac
done
# 
if [[ ! -z $iopt ]]
then
{
wd=$(pwd)
basename "$(test -L "$0" && readlink "$0" || echo "$0")" > /tmp/scriptname
scriptname=$(echo -e -n $wd/ && cat /tmp/scriptname)
#增加执行权限/usr/bin/chmod +x /usr/bin/monitor 由gjimmyz增加
su -c "cp $scriptname /usr/bin/monitor && /usr/bin/chmod +x /usr/bin/monitor" root && echo "Congratulations! Script Installed, now run monitor Command" || echo "Installation failed"
}
fi

if [[ ! -z $vopt ]]
then
{
echo -e "tecmint_monitor version 0.1\nDesigned by Tecmint.com\nReleased Under Apache 2.0 License"
}
fi
if [[ ! -z $hopt ]]
then
{
echo -e "-i                                Install script"
echo -e "-v                                Print version information and exit"
echo -e "-h                                Print help (this information) and exit"
}
fi

if [[ $# -eq 0 ]]
then
{
clear

unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage

# Define Variable tecreset
tecreset=$(tput sgr0)

# Check if connected to Internet or not
ping -c 1 www.baidu.com &> /dev/null && echo -e '\E[32m'"Internet: $tecreset Connected" || echo -e '\E[32m'"Internet: $tecreset Disconnected"

# Check OS Type
os=$(uname -o)
echo -e '\E[32m'"Operating System Type :" $tecreset $os

# Check OS Release Version and Name
###################################
OS=`uname -s`
REV=`uname -r`
MACH=`uname -m`

GetVersionFromFile()
{
    VERSION=`cat $1 | tr "\n" ' ' | sed s/.*VERSION.*=\ // `
}

if [ "${OS}" = "SunOS" ] ; then
    OS=Solaris
    ARCH=`uname -p`
    OSSTR="${OS} ${REV}(${ARCH} `uname -v`)"
elif [ "${OS}" = "AIX" ] ; then
    OSSTR="${OS} `oslevel` (`oslevel -r`)"
elif [ "${OS}" = "Linux" ] ; then
    KERNEL=`uname -r`
    if [ -f /etc/redhat-release ] ; then
        DIST='RedHat'
        PSUEDONAME=`cat /etc/redhat-release | sed s/.*\(// | sed s/\)//`
        REV=`cat /etc/redhat-release | sed s/.*release\ // | sed s/\ .*//`
    elif [ -f /etc/SuSE-release ] ; then
        DIST=`cat /etc/SuSE-release | tr "\n" ' '| sed s/VERSION.*//`
        REV=`cat /etc/SuSE-release | tr "\n" ' ' | sed s/.*=\ //`
    elif [ -f /etc/mandrake-release ] ; then
        DIST='Mandrake'
        PSUEDONAME=`cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//`
        REV=`cat /etc/mandrake-release | sed s/.*release\ // | sed s/\ .*//`
    elif [ -f /etc/debian_version ] ; then
        DIST="Debian `cat /etc/debian_version`"
        REV=""

    fi
    if ${OSSTR} [ -f /etc/UnitedLinux-release ] ; then
        DIST="${DIST}[`cat /etc/UnitedLinux-release | tr "\n" ' ' | sed s/VERSION.*//`]"
    fi

    OSSTR="${OS} ${DIST} ${REV}(${PSUEDONAME} ${KERNEL} ${MACH})"

fi

##################################
#cat /etc/os-release | grep 'NAME\|VERSION' | grep -v 'VERSION_ID' | grep -v 'PRETTY_NAME' > /tmp/osrelease
#echo -n -e '\E[32m'"OS Name :" $tecreset  && cat /tmp/osrelease | grep -v "VERSION" | grep -v CPE_NAME | cut -f2 -d\"
#echo -n -e '\E[32m'"OS Version :" $tecreset && cat /tmp/osrelease | grep -v "NAME" | grep -v CT_VERSION | cut -f2 -d\"
echo -e '\E[32m'"OS Version :" $tecreset $OSSTR 

architecture=$(uname -m)
echo -e '\E[32m'"Architecture :" $tecreset $architecture


kernelrelease=$(uname -r)
echo -e '\E[32m'"Kernel Release :" $tecreset $kernelrelease


echo -e '\E[32m'"Hostname :" $tecreset $HOSTNAME


internalip=$(hostname -I)
echo -e '\E[32m'"Internal IP :" $tecreset $internalip

#加上超时时间 然后判断下 由gjimmyz增加
externalip=$(curl -s --connect-timeout 2 ipecho.net/plain;echo)
if [[ ! -z ${externalip} ]]
then
    echo -e '\E[32m'"External IP : $tecreset "$externalip
else
    echo -e '\E[32m'"External IP : $tecreset "可能存在请求超时，请再一次执行monitor命令试试!
fi

nameservers=$(cat /etc/resolv.conf | sed '1 d' | awk '{print $2}')
echo -e '\E[32m'"Name Servers :" $tecreset $nameservers 


who>/tmp/who
echo -e '\E[32m'"Logged In users :" $tecreset && cat /tmp/who 


free -h | grep -v + > /tmp/ramcache
echo -e '\E[32m'"Ram Usages :" $tecreset
cat /tmp/ramcache | grep -v "Swap"
echo -e '\E[32m'"Swap Usages :" $tecreset
cat /tmp/ramcache | grep -v "Mem"


df -h| grep 'Filesystem\|/dev/sda*' > /tmp/diskusage
echo -e '\E[32m'"Disk Usages :" $tecreset 
cat /tmp/diskusage


loadaverage=$(top -n 1 -b | grep "load average:" | awk '{print $10 $11 $12}')
echo -e '\E[32m'"Load Average :" $tecreset $loadaverage


tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
echo -e '\E[32m'"System Uptime Days/(HH:MM) :" $tecreset $tecuptime


unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage

rm /tmp/who /tmp/ramcache /tmp/diskusage
}
fi
shift $(($OPTIND -1))

效果
Internet:  Connected
Operating System Type :  GNU/Linux
OS Version :  Linux RedHat 7.6.1810(Core 3.10.0-957.el7.x86_64 x86_64)
Architecture :  x86_64
Kernel Release :  3.10.0-957.el7.x86_64
Hostname :  localhost.localdomain
Internal IP :  192.168.0.107
External IP :  101.85.213.234
Name Servers :  202.96.209.5 202.96.209.133
Logged In users : 
root     pts/0        2020-04-06 16:09 (192.168.0.101)
root     pts/1        2020-04-07 20:17 (192.168.0.101)
Ram Usages : 
              total        used        free      shared  buff/cache   available
Mem:           972M         73M        707M        7.6M        191M        725M
Swap Usages : 
              total        used        free      shared  buff/cache   available
Swap:            0B          0B          0B
Disk Usages : 
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       197G  2.2G  185G   2% /
/dev/sda1       190M   95M   81M  54% /boot
Load Average :  loadaverage:0.00,
System Uptime Days/(HH:MM) :  1 day
