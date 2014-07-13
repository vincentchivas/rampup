#!/bin/bash
mail='/home/huangbin/mail.txt'

if [ ! -f '$mail' ] ;  then 
    touch '$mail'
fi    

if [ -f '$mail' ] ;  then 
    rm   '/home/huangbin/mail.txt'
fi

echo '占用内存最高的前五个进程' >>mail.txt

ps aux|head -1 >> mail.txt
ps aux|grep -v PID|sort -k4nr|head -n 5 >> mail.txt

echo ' ' >> mail.txt
echo '当前正在被占用的网络端口，端口号以及进程ID' >> mail.txt

netstat -atupnl >> mail.txt

echo ' '  >> mail.txt
echo '当前用户账户主目录文件总大小' >> mail.txt

du -sh >> mail.txt

mail -s 'the first task of rampup!'   bhuang@bainainfo.com < mail.txt
echo 'done!'

