#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

'''
$nginxConfPath
$nginxErrorLogPath
$nginxPidPath
$nginxUpStreamList
$includePath
'''

from Gyrfalcon.configure.GlobalConfigure import *
from service.configure.TornadoNginxSettings import *

nginxConfPath = "$nginxConfPath"
nginxErrorLogPath = "$nginxErrorLogPath"
nginxPidPath = "$nginxPidPath"
nginxUpStreamList = "$nginxUpStreamList"
includePath = "$includePath"
rootPath = "$rootPath"

NginxSetting = {
    rootPath : project_path,
    nginxConfPath : nginx_path,
    nginxErrorLogPath : path.join(log_path,"nginx/error.log"),
    nginxPidPath : path.join(nginx_pid_path,"nginx.pid"),
    includePath : path.join(nginx_path,"gfplatform/*.conf"),
}

gfMakeDirs(NginxSetting[nginxConfPath])
gfMakeDirs(NginxSetting[nginxErrorLogPath], touch_file=True)
gfMakeDirs(NginxSetting[nginxPidPath])
