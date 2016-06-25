#!/bin/bash

# 系统名称
sysOS=`uname -s`;

# 当前路径
dirPath=$(cd `dirname $0`; pwd);

sh $dirPath/platforms/$sysOS/GyrfalconStart.command $dirPath $sysOS;

python3 $dirPath/../Gyrfalcon/Gyrfalcon.py;

if [ $? -ne 0 ]
then
  echo "   [ 服务启动失败 ]   ";
else
  echo "   [ 服务启动成功 ]   ";
  echo "请打开浏览器输入
    http://localhost/admin
    或者
    http://127.0.0.1/admin
    进入后台
    "
fi
