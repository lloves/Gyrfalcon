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

nginxConfPath = "${product_name}_nginxConfPath".format(product_name=product_name.lower())
nginxErrorLogPath = "${product_name}_nginxErrorLogPath".format(product_name=product_name.lower())
nginxPidPath = "${product_name}_nginxPidPath".format(product_name=product_name.lower())
nginxUpStreamList = "${product_name}_nginxUpStreamList".format(product_name=product_name.lower())
includePath = "${product_name}_includePath".format(product_name=product_name.lower())
rootPath = "${product_name}_rootPath".format(product_name=product_name.lower())
domainKey = "${product_name}_domain".format(product_name=product_name.lower())

NginxSetting = {
    rootPath : project_path,
    nginxConfPath : nginx_path,
    domainKey : domain,
    nginxErrorLogPath : path.join(global_nginx_path,"log/error.log"),
    nginxPidPath : path.join(nginx_pid_path,"nginx.pid"),
    includePath : path.join(nginx_path,"servers/*.conf"),
}

gfMakeDirs(NginxSetting[nginxConfPath])
gfMakeDirs(NginxSetting[nginxErrorLogPath], touch_file=True)
gfMakeDirs(NginxSetting[nginxPidPath])
