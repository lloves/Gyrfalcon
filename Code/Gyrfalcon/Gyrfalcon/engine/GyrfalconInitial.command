#!/bin/bash

# 系统名称
sysOS=`uname -s`;

# 当前路径
dirPath=$(cd `dirname $0`; pwd);

# 关闭服务
sh $dirPath/GyrfalconStop.command;

# 初始化服务
sh $dirPath/platforms/$sysOS/GyrfalconInitial.command;

echo "正在初始化后台...";
export PYTHONPATH=$(cd $dirPath/..; pwd);
python3 $dirPath/tools/djangoinitial.py;

echo "是否创建admin超级用户[Y/n]:";
read shouldCreateSuperUser;
if [ "$shouldCreateSuperUser"x == "Y"x ]
then
  $dirPath/GyrfalconShell.command createsuperuser;
fi

echo "服务初始化完成";

sh $dirPath/GyrfalconStart.command;
