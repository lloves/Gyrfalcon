#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

import os
from os import path
import sys
import platform

# 创建目录或者文件
def gfMakeDirs(path_name, touch_file=False, root=False):
	'''
	path_name: 对应文件目录名
	touch_file: 是否创建文件，True=创建文件，False=创建目录
	'''
	sudo = ''
	if root:
		sudo = 'sudo'

	if os.path.exists(path_name):
		return

	if touch_file == True:
		if os.path.exists(os.path.dirname(path_name)) == False:
			os.makedirs(os.path.dirname(path_name))
		os.system("{sudo} touch {path_name}".format(sudo=sudo, path_name=path_name))
	else:
		os.system('{sudo} mkdir -p {path_name}'.format(sudo=sudo, path_name=path_name))

def gfOwnDir(path_name, user=None):

	if user == None:
		os.system('sudo chown $USER {path_name}'.format(path_name=path_name))
	else:
		os.system('sudo chown {user} {path_name}'.format(user=user, path_name=path_name))

def gfModeDir(path_name, mode="755"):
	os.system('sudo chmod {mode} {path_name}'.format(mode=mode, path_name=path_name))


# 是否使用测试模式
debug = False

######################## IP设置 ########################

# tornado服务的ip地址
tornado_ip = '127.0.0.1'

# django服务的ip地址
django_ip = '127.0.0.1'

# 端口

######################## 测试模式 ########################

#  测试模式下tornado端口
debug_tornado_port = 8984
#  测试模式下django端口
debug_django_port = 8981

#  域名
domain = 'localhost'

######################## 正式模式 ########################


# 正式模式下django端口
release_django_port = 8982

# 正是模式下tornado进程端口
tornado_ports = [
	8991,
	8992,
	8993,
	8994,
]

######################## 项目 ###########################

# 项目名
project_name = "Gyrfalcon";

# 产品名称
product_name = "Gyrfalcon";

# 后台名
django_project_name="backend"

######################## 路径 ###########################

# 项目路径
project_path = path.realpath(path.join(path.dirname(__file__), "../../"))
gfMakeDirs(project_path)

# 核心代码路径
subproject_path = path.join(project_path,project_name)
gfMakeDirs(subproject_path)

# 模板路径
template_path = path.join(project_path,"template")
gfMakeDirs(template_path)

# 静态文件路径 包括静态图片资源，css，js
static_path = path.join(project_path,"static")
gfMakeDirs(static_path)

# 用户资源储存路径
media_path = path.join(project_path,"media")
gfMakeDirs(media_path)

# django 路径
django_path = path.join(subproject_path, "main/"+django_project_name)
gfMakeDirs(django_path)

# 工作区路径
workspace_path = path.join(project_path, "workspace")
gfMakeDirs(workspace_path)

# configure 路径
configure_path = path.join(subproject_path, "configure")
gfMakeDirs(configure_path)

# 服务路径
service_path = path.join(project_path, "service")
gfMakeDirs(service_path)

####################### 部署 ###########################

# 公共配置
global_config_path = "/etc/"+project_name
gfMakeDirs(global_config_path, root=True)
gfOwnDir(global_config_path)
gfModeDir(global_config_path)

# 公共 nginx 配置路径
global_nginx_path = path.join(global_config_path, "nginx")
gfMakeDirs(global_nginx_path, root=True)
gfOwnDir(global_nginx_path)
gfModeDir(global_nginx_path)

# 服务器配置路径
service_configure_path = path.join(service_path, "configure")
gfMakeDirs(service_configure_path)

# 服务器启动配置文件路径
service_profile_path = path.join(service_path, "profile")
gfMakeDirs(service_profile_path)

# 日志路径
log_path = path.join(workspace_path, "log")
gfMakeDirs(log_path)

# 项目 nginx 配置模板
nginx_path = path.join(service_profile_path, "nginx")
gfMakeDirs(nginx_path)


# nginx pid 路径
nginx_pid_path = path.join(nginx_path, "pid")
gfMakeDirs(nginx_pid_path)

# nginx 主配置文件路径
nginx_conf_path = path.join(nginx_path, "{project_name}_nginx.conf".format(project_name=project_name.lower()))
gfMakeDirs(nginx_conf_path, touch_file=True)

# nginx 主配置模板文件路径
nginx_conf_template_path = path.join(nginx_path, "{project_name}_nginx_template.conf".format(project_name=project_name.lower()))
gfMakeDirs(nginx_conf_template_path, touch_file=True)


# nginx 主配置全局文件路径
global_nginx_conf_path = path.join(global_nginx_path, "{project_name}_nginx.conf".format(project_name=project_name.lower()))
gfMakeDirs(global_nginx_conf_path, touch_file=True)

# nginx 配置文件路径
nginx_project_conf_path = path.join(nginx_path, 'servers')
gfMakeDirs(nginx_project_conf_path)

# nginx 配置通用文件路径
global_nginx_project_conf_path = path.join(global_nginx_path, 'servers')
gfMakeDirs(global_nginx_project_conf_path)

# tornado 日志路径
tornado_log_path = path.join(log_path,"tornado/tornado.log")
gfMakeDirs(tornado_log_path, touch_file=True)

# django管理器路径
django_manage_path = path.join(django_path,"manage.py")

########################### 数据库 ###########################

# 数据库命名不能超过14个长度
if debug == False:
########################### 测试模式 ###########################
	# 数据库地址
	dbhost = "localhost"
	# 数据库名称
	dbname = "Gyrfalcon_tes1"
	# 数据库用户名
	dbuser = "Gyrfalcon"
	# 数据库密码
	dbpassword = "Gyrfalcon_pwd"
else:
########################### 正式模式 ###########################
	dbhost = "localhost"
	dbname = "Gyrfalcon_test1"
	dbuser = "Gyrfalcon"
	dbpassword = "Gyrfalcon_pwd"

######################## 其他 ###############################
# des加密密码
desPassword = "bfae43b0"
