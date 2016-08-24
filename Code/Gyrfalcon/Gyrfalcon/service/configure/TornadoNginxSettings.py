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

tornadoDomains = "${product_name}_tornadoDomains".format(product_name=product_name.lower())
tornadoRootPath = "${product_name}_tornadoRootPath".format(product_name=product_name.lower())
tornadoUpStream = "${product_name}_tornadoUpStream".format(product_name=product_name.lower())
tornadoStaticPath = "${product_name}_tornadoStaticPath".format(product_name=product_name.lower())
tornadoAdminStaticPath = "${product_name}_tornadoAdminStaticPath".format(product_name=product_name.lower())
tornadoMediaPath = "${product_name}_tornadoMediaPath".format(product_name=product_name.lower())

tornadoUpStreamName = product_name.lower()+"_tornadoes"
tornadoes_ip = tornado_ip
tornadoUpStreamList = []

for port in tornado_ports:
    tornadoUpStreamList.append("server "+tornadoes_ip+":"+str(port))
tornadoUpStreamString = "".join([ \
    "upstream "+tornadoUpStreamName +" { \n", \
    "; \n".join(tornadoUpStreamList)+"; \n",
    "}",
])

TornadoNginxSetting = {

    tornadoDomains:tornado_ip,
    tornadoRootPath:path.join(subproject_path,"main/site"),
    tornadoUpStream:tornadoUpStreamName,
    tornadoStaticPath:static_path,
    tornadoAdminStaticPath:path.join(static_path,"admin"),
    tornadoMediaPath:media_path,
}
