#!/bin/bash


# 系统名称
sysOS=`uname -s`;

# 当前路径
dirPath=$(cd `dirname $0`; pwd);

sh $dirPath/GyrfalconStop.command;
sh $dirPath/GyrfalconStart.command;
