#!/bin/bash
# debug模式
debug=1;

# 当前路径
dirPath=$(cd `dirname $0`; pwd);

osinstaller="brew install";
# 系统名称
sysOS=`uname -s`;

##### 工具  #####

# $1 软件名
# $2 安装函数
# $3 检测软件的shell语句
function gfInstall() {
	echo " 检测 [ $1 ]...";
	eval $3 1>/dev/null 2>/dev/null;
	if [ $? -ne 0 ]
	then
		echo " [ $1 ]不存在, 开始安装...";
		$2;
		echo " [ $1 ] 安装成功
		";
	else
		echo " [ $1 ] 检测完成
		";
	fi
}

# brew安装函数
function brewIns() {
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)";
}
# 安装Brew
gfInstall Brew brewIns "brew -v";

# wget安装函数
function wgetIns() {
	$osinstaller wget;
}
# 安装wget
gfInstall wget wgetIns "wget --help";

# python安装函数
function pythonIns() {
	if [ $sysOS == "Darwin" ]
	then
		brew unlink python3;
		brew uninstall python3 --force;
		brew install readline;
		brew install zlib;
		brew install openssl
		brew install python3;
	fi
}
# 安装Python3.4.3
gfInstall Python3 pythonIns "python3 -V";

# mysql安装函数
function mysqlIns() {
	mysqlUrl="http://cdn.mysql.com//Downloads/MySQL-5.6/mysql-5.6.32-linux-glibc2.5-x86_64.tar.gz";
	if [ $sysOS == "Darwin" ]
	then
		mysqlUrl="http://cdn.mysql.com//Downloads/MySQL-5.6/mysql-5.6.32-osx10.11-x86_64.tar.gz";
	fi

	if [ ! -f $dirPath/packages/mysql-5.6.32-osx10.11-x86_64.tar.gz ]
	then
		wget -P $dirPath/packages $mysqlUrl;
	fi

	sudo rm -rf /usr/local/mysql*;
	sudo rm -rf /usr/local/lib/libmysql*;
	sudo rm -rf /usr/local/bin/mysql*;
	sudo tar xvf $dirPath/packages/mysql-5.6.32-osx10.11-x86_64.tar.gz -C /usr/local/;
 	sudo mv /usr/local/mysql-5.6.32-osx10.11-x86_64/ /usr/local/mysql;
	sudo ln -sv /usr/local/mysql/bin/mysql* /usr/local/bin;
	sudo ln -sv /usr/local/mysql/lib/libmysql* /usr/local/lib;
	sudo ln -sv /usr/local/mysql/support-files/mysql.server /usr/local/bin/;
	sudo chown -R $USER:admin /usr/local/mysql;
	cd /usr/local/mysql;
	./scripts/mysql_install_db --user=$USER --basedir=/usr/local/mysql;
}
# 安装Mysql5.6
gfInstall MySQL5.6 mysqlIns "mysql --help";

# nginx安装函数
function nginxIns() {
	$osinstaller zlib;
	$osinstaller openssl;
	$osinstaller pcre;
	brew tap homebrew/nginx;
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
	sudo python2.7 setup.py install;
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

	tar xvf $dirPath/packages/uwsgi-2.0.12.tar.gz -C $dirPath/packages;
	cd $dirPath/packages/uwsgi-2.0.12/;
	CPPFLAGS="-I/usr/local/opt/openssl/include -I/usr/local/opt/zlib/include" LDFLAGS="-L/usr/local/opt/openssl/lib -L/usr/local/opt/zlib/lib" CC=gcc python3 uwsgiconfig.py --build;
	CPPFLAGS="-I/usr/local/opt/openssl/include -I/usr/local/opt/zlib/include" LDFLAGS="-L/usr/local/opt/openssl/lib -L/usr/local/opt/zlib/lib" CC=gcc python3 uwsgiconfig.py --plugin plugins/python core py35;
	sudo mkdir /usr/local/lib/uwsgi 2>/dev/null;
	sudo cp -rf ./py35_plugin.so /usr/local/lib/uwsgi;
	sudo cp -rf ./uwsgi /usr/local/bin;
	cd ../;
	sudo rm -rf $dirPath/packages/uwsgi*/;
}
# 安装uwsgi
gfInstall uwsgi uwsgiIns "uwsgi --version";

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

	sudo sed -e 's/python/python3/' /usr/local/lib/python*/site-packages/django/bin/django-admin.py > /usr/local/bin/django-admin;
}
# 安装django
gfInstall django-admin djangoAdminIns "django-admin";


# torndb安装函数
function torndbIns() {

	sudo pip3 install torndb==0.3;
torndbOrg=" use_unicode=True,";
torndbTgt="";
sudo sed -i -e "s/$torndbOrg/$torndbTgt/g" /usr/local/lib/python3*/site-packages/torndb.py;
}
# 安装torndb
gfInstall torndb torndbIns "python3 -c \"import torndb\"";

# pillow安装函数
function pillowIns() {

	sudo pip3 install pillow==3.1.0;
}
# 安装pillow
gfInstall pillow pillowIns "python3 -c \"from PIL import Image\"";

echo "启动数据库...";
mysql.server start;

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
	brew install libxml2;
	C_INCLUDE_PATH=/usr/local/opt/libxml2/include/libxml2 sudo pip3 install lxml;
	sudo pip3 install pandas;
	sudo pip3 install tushare;
}

# 安装tushare
gfInstall tushare tushareIns "python3 -c \"import tushare\""


# scrapy 安装函数
function scrapyIns() {
	brew install libxml2;
	C_INCLUDE_PATH=/usr/local/opt/libxml2/include/libxml2 sudo pip3 install scrapy;
}

# 安装scrapy
gfInstall scrapy scrapyIns "scrapy 2>/dev/null;";


# BeautifulSoap4 安装函数
function beautifulSoap4Ins() {
	sudo pip3 install BeautifulSoap4;
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
mysql.server start;
if [ $? -ne 0 ]
then
	echo "数据库服务打开失败";
fi

sh $dirPath/GyrfalconStart.command;
