#!/usr/bin/env bash

# debug模式
debug=1;

# 当前路径
dirPath=$(cd `dirname $0`; pwd);

. $dirPath/GyrfalconProfile.command;

$osinstaller -h 2>/dev/null 1>/dev/null;
if [ $? -ne 0 ]
then
  echo "
  如果你在Ubuntu系统下请输入sudo apt-get install
  如果你在Centos系统下请输入sudo yum install
  或者 你可以在 $dirPath/GyrfalconProfile.command 文件中修改配置
  请输入安装命令：";
  read osinstaller;
fi

$mysqlCommand status 2>/dev/null 1>/dev/null;
if [ $? -ne 0 ]
then
  echo "
  如果你安装了mariadb请输入sudo service mariadb
  如果你安装了mysqldb系统下请输入sudo service mysql
  如果你的数据库启动指令是mysql.server start.
  那么你要输入mysql.server
  或者 你可以在 $dirPath/GyrfalconProfile.command 文件中修改配置
  请输入数据库命令：";
  read mysqlCommand;
fi

echo "
#! /bin/bash
osinstaller=\"$osinstaller\"
mysqlCommand=\"$mysqlCommand\"
" > $dirPath/GyrfalconProfile.command;

# 系统名称
sysOS=`uname -s`;

##### 工具  #####

# $1 软件名
# $2 安装函数
# $3 检测软件的shell语句

function gfInstall() {
  echo "检测 [ $1 ]...";
  eval $3 1>/dev/null 2>/dev/null;
  if [ $? -ne 0 ]
  then
    echo "[ $1 ]不存在, 开始安装...";
    $2;
    echo "[ $1 ] 安装成功";
  else
    echo "[ $1 ] 检测完成";
  fi
};

sh $dirPath/GyrfalconStop.command;

# wget安装函数
function wgetIns() {
  $osinstaller wget;
}
# 安装wget
gfInstall wget wgetIns "wget --help";

# python3安装函数
function pythonIns() {

  $osinstaller zlib-devel bzip2-devel openssl-devel ncurses-devel;
  python3 -V 2>/dev/null 1>/dev/null;
  if [ $? -ne 0 ]
  then
    if [ ! -f $dirPath/packages/Python-3.5.2.tgz ]
    then
      wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz -P $dirPath/packages;
    fi
    tar xvf $dirPath/packages/Python-3.5.2.tgz -C $dirPath/packages;
    cd $dirPath/packages/Python-3.5.2;
    CFLAGS="$CFLAGS -O3 -fPIC" CXXFLAGS="$CXXFLAGS -fPIC" ./configure;
    sudo make && sudo make install;
    cd $dirPath;
    sudo rm -rf $dirPath/packages/Python-3.5.2;
    sudo rm -rf /usr/bin/python3;
    sudo rm -rf /usr/bin/pip3;
    sudo ln -sv /usr/local/bin/python3 /usr/bin/python3;
    sudo ln -sv /usr/local/bin/pip3 /usr/bin/pip3;
  fi
}
# 安装Python3.5.2
gfInstall Python3.5.2 pythonIns "python3 -V";

# mysql安装函数
function mysqlIns() {
  if [ "$osinstaller" == "sudo yum install" ];
  then
    $osinstaller mariadb mariadb-server libmariadbclient*;
    sudo systemctl enable mariadb.service;
  elif [ "$osinstaller" == "sudo apt-get install" ];
  then
    $osinstaller mariadb mariadb-server libmariadbclient*;
    $osinstaller mysql mysql-server libmysqlclient*;
  fi
}
# 安装Mysql5.6
gfInstall MySQL5.6 mysqlIns "mysql --help";

# nginx安装函数
function nginxIns() {
  $osinstaller nginx;
}
# 安装nginx
gfInstall NginX nginxIns "nginx -v";

# supervisor安装函数
function supervisorIns() {
  if [ ! -f $dirPath/packages/supervisor-3.2.0.tar.gz ]
  then
    wget https://pypi.python.org/packages/source/s/supervisor/supervisor-3.2.0.tar.gz -P $dirPath/packages;
  fi

  tar xvf $dirPath/packages/supervisor-3.2.0.tar.gz -C $dirPath/packages;
  cd $dirPath/packages/supervisor-3.2.0;
  sudo python2 setup.py install;
  cd $dirPath;
  sudo rm -rf $dirPath/packages/supervisor-3.2.0/;
}

# 安装supervisor
gfInstall Supervisor3.2.0 supervisorIns "supervisord -v";

# uwsgi安装函数
function uwsgiIns() {
  if [ ! -f $dirPath/packages/uwsgi-2.0.12.tar.gz ]
  then
    wget http://projects.unbit.it/downloads/uwsgi-2.0.12.tar.gz -P $dirPath/packages;
  fi
  $osinstaller libxml*;
  tar xvf $dirPath/packages/uwsgi-2.0.12.tar.gz -C $dirPath/packages;
  cd $dirPath/packages/uwsgi-2.0.12/
  sudo CFLAGS="-O3 -fPIC" CC=gcc python3 ./uwsgiconfig.py --build;
  sudo CFLAGS="-O3 -fPIC" CC=gcc python3 ./uwsgiconfig.py --plugin plugins/python core py35;
  sudo mkdir -p /usr/local/lib/uwsgi 2>/dev/null;
  sudo cp -rf ./py35_plugin.so /usr/local/lib/uwsgi;
  sudo cp -rf uwsgi /usr/local/bin;
  cd ../;
  sudo rm -rf $dirPath/packages/uwsgi*/;
  sudo ln -sv /usr/local/bin/uwsgi /usr/bin/;
}
# 安装uwsgi
gfInstall uwsgi uwsgiIns "uwsgi --version";

# bpython安装函数
function bPythonIns() {

  sudo pip3 install bpython;
}
# 安装bPython
gfInstall bPython bPythonIns "bpython -h";

# iPython安装函数
function iPythonIns() {
  sudo pip3 install ipython;
}
# 安装iPython
gfInstall iPython iPythonIns "ipython -h";

# tornado安装函数
function tornadoIns() {

  sudo pip3 install tornado==4.2;
}

# 安装tornado
gfInstall tornado tornadoIns "python3 -c \"import tornado\"";

# django安装函数
function djangoIns() {
  sudo pip3 install django==1.9.1;
}
# 安装django
gfInstall django djangoIns "python3 -c \"import django\"";

# django安装函数
function djangoAdminIns() {
  sudo sed -e 's/python/python3/' /usr/local/lib/python3.5/site-packages/django/bin/django-admin.py > /usr/local/bin/django-admin;
}
# 安装django
gfInstall django-admin djangoAdminIns "django-admin";


# torndb安装函数
function torndbIns() {
  sudo pip3 install torndb==0.3;
}

torndbOrg=" use_unicode=True,";
torndbTgt="";
sudo sed -i -e "s/$torndbOrg/$torndbTgt/g" /usr/lib/python3.5/site-packages/torndb.py 2>/dev/null 1>/dev/null;
sudo sed -i -e "s/$torndbOrg/$torndbTgt/g" /usr/local/lib/python3.5/site-packages/torndb.py 2>/dev/null 1>/dev/null;
sudo sed -i -e "s/$torndbOrg/$torndbTgt/g" /usr/lib/python3.5/dist-packages/torndb.py 2>/dev/null 1>/dev/null;
sudo sed -i -e "s/$torndbOrg/$torndbTgt/g" /usr/local/lib/python3.5/dist-packages/torndb.py 2>/dev/null 1>/dev/null;
# 安装torndb
gfInstall torndb torndbIns "python3 -c 'import torndb'";

# pillow安装函数
function pillowIns() {
  $osinstaller libjpeg* libpng*;
  sudo pip3 install pillow;
}
# 安装pillow
gfInstall pillow pillowIns "python3 -c \"from PIL import Image\"";

echo "启动数据库...";
$mysqlCommand start;

# MySQLdb安装函数
function mySQLdbIns() {
  DYLD_LIBRARY_PATH="/usr/local/mysql/lib:-L/usr/local/mysql/lib/" sudo pip3 install $dirPath/packages/MySQL-for-Python-3.zip;
}
# 安装MySQLdb
gfInstall MySQLdb mySQLdbIns "python3 -c \"import MySQLdb\"";

# pycrypto 安装函数
function pycryptoIns() {
  sudo pip3 install pycrypto;
}

# 安装pycrypto
gfInstall pycrypto pycryptoIns "python3 -c \"import Crypto\""

# pyDes 安装函数
function pyDesIns() {
  sudo pip3 install pyDes;
}

# 安装pyDes
gfInstall pyDesIns pyDesIns "python3 -c \"import pyDes\""

# tushare 安装函数
function tushareIns() {
    sudo pip3 install lxml;
    sudo pip3 install tushare;
}

# 安装tushare
gfInstall tushareIns pyDesIns "python3 -c \"import tushare\"";

# scrapy 安装函数
function scrapyIns() {
  $osinstaller install libssl-devel;
  sudo pip3 install scrapy;
}

# 安装tushare
gfInstall scrapy scrapyIns "scrapy 2>/dev/null;";

# BeautifulSoap4 安装函数
function beautifulSoap4Ins() {
  sudo pip3 install bs4;
}

# 安装BeautifulSoap4
gfInstall BeautifulSoap4 beautifulSoap4Ins "python3 -c \"import bs4\"";

function pytzIns() {
  sudo pip3 install pytz;
}
gfInstall pytz pytzIns "python3 -c \"import pytz\""

echo "初始化环境完成, 重置服务"
sh $dirPath/GyrfalconStop.command;

echo "试图开启数据库服务";
$mysqlCommand start;
if [ $? -ne 0 ]
then
  echo "数据库服务打开失败";
fi

sh $dirPath/GyrfalconStart.command;
