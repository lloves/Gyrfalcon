#!/bin/bash

dirPath=$(cd `dirname $0`; pwd);

echo "[ 正在关闭服务 ]"
mysql.server stop 2>/dev/null;
