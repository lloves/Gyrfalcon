#!/bin/bash

# 进行tornado配置初始化后 根据tornado配置初始化django配置，最后获得2者配置后开启nginx

dirPath=$(cd `dirname $0`; pwd);
echo "  [ 服务启动中 ]  ";

. $dirPath/GyrfalconProfile.command
$mysqlCommand start;

