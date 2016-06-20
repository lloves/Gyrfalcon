#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

import os
from os import path
import sys

def gfMakeDirs(path_name, touch_file=False):
	if len(os.path.splitext(path_name)[1]) > 0:
		if os.path.exists(os.path.dirname(path_name)) == False:
			os.makedirs(os.path.dirname(path_name), exist_ok=True)
		if touch_file == True and os.path.exists(path_name) == False:
			os.system("touch {path_name}".format(path_name=path_name))
	else:
		if os.path.exists(path_name) == False:
			os.makedirs(path_name, exist_ok=True)


# 是否使用测试模式
debug = False

# 端口

debug_tornado_port = 8984
debug_django_port = 8981

release_tornado_port = 8983
release_django_port = 8982

# tornado进程端口
tornado_ports = [
	8991,
	8992,
	8993,
	8994,
]

######################## 项目 ###########################

# 项目名
project_name = "Gyrfalcon";

# 后台名
django_project_name="backend"

######################## 路径 ###########################

# 项目路径
project_path = path.realpath(path.join(path.dirname(__file__), "../../../"+project_name))
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

# 服务器配置路径
service_configure_path = path.join(service_path, "configure")
gfMakeDirs(service_configure_path)

# 服务器启动配置文件路径
service_profile_path = path.join(service_path, "profile")
gfMakeDirs(service_profile_path)

# 日志路径
log_path = path.join(workspace_path, "log")
gfMakeDirs(log_path)

# nginx 路径
nginx_path = path.join(service_profile_path, "nginx")
gfMakeDirs(nginx_path)

# nginx pid 路径
nginx_pid_path = path.join(nginx_path, "pid")
gfMakeDirs(nginx_pid_path)

# nginx 主配置文件路径
import platform
osname = platform.uname()[0]
nginx_conf_path = path.join(nginx_path, "nginx.conf")
if osname == "Darwin":
	nginx_conf_path = path.join(nginx_path, "nginx_bsd.conf")
gfMakeDirs(nginx_conf_path)

# nginx GF配置文件路径
nginx_project_conf_path = path.join(nginx_path, project_name.lower())
gfMakeDirs(nginx_project_conf_path)

tornado_log_path = path.join(log_path,"tornado/tornado.log")
gfMakeDirs(tornado_log_path, touch_file=True)

# django管理器路径
django_manage_path = path.join(django_path,"manage.py")




########################### 数据库 ###########################

# 数据库命名不能超过14个长度
if debug == False:
	dbhost = "localhost"
	dbname = "Gyrfalcon"
	dbuser = "Gyrfalcon"
	dbpassword = "Gyrfalcon_pwd"
else:
	dbhost = "localhost"
	dbname = "Gyrfalcon"
	dbuser = "Gyrfalcon"
	dbpassword = "Gyrfalcon_pwd"


######################## 其他 ###############################

desPassword = "bfae43b0"
