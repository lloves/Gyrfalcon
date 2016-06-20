#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

'''
$tornadoDomains
$tornadoRootPath
$tornadoUpStream
$tornadoStaticPath
$tornadoAdminStaticPath
$tornadoMediaPath
'''

from Gyrfalcon.configure.GlobalConfigure import *

tornadoDomains = "$tornadoDomains"
tornadoRootPath = "$tornadoRootPath"
tornadoUpStream = "$tornadoUpStream"
tornadoStaticPath = "$tornadoStaticPath"
tornadoAdminStaticPath = "$tornadoAdminStaticPath"
tornadoMediaPath = "$tornadoMediaPath"

tornadoUpStreamName = "tornadoes"
tornadoes_ip = "127.0.0.1"
tornadoUpStreamList = []

for port in tornado_ports:
    tornadoUpStreamList.append("server "+tornadoes_ip+":"+str(port))
tornadoUpStreamString = "".join([ \
    "upstream "+tornadoUpStreamName +" { \n", \
    "; \n".join(tornadoUpStreamList)+"; \n",
    "}",
])

TornadoNginxSetting = {

    tornadoDomains:"localhost",
    tornadoRootPath:path.join(subproject_path,"main/site"),
    tornadoUpStream:tornadoUpStreamName,
    tornadoStaticPath:static_path,
    tornadoAdminStaticPath:path.join(static_path,"admin"),
    tornadoMediaPath:media_path,
}
