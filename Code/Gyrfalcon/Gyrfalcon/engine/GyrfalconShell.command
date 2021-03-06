#!/bin/bash

# 数据调试命令行

dirPath=$(cd `dirname $0`; pwd);

cd $dirPath/../..;

sudo chown -R $USER $dirPath/../..;

export PYTHONPATH=$PYTHONPATH:$(cd $dirPath/..; pwd);
python3 $dirPath/tools/shell.py $0 $1 $2;
