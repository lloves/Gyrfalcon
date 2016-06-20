#!/bin/bash

dirPath=$(cd `dirname $0`; pwd);

echo "  [ 正在关闭服务 ]  "
. $dirPath/GyrfalconProfile.command;
$mysqlCommand stop;
