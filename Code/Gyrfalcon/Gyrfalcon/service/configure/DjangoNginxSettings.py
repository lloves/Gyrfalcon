#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

'''
$djangoDomains
$djangoRootPath
$djangoUwsgiPass
$djangoStaticPath
$djangoAdminStaticPath
$djangoMediaPath
'''

from Gyrfalcon.configure.GlobalConfigure import *

djangoDomains = "${product_name}_djangoDomains".format(product_name=product_name.lower())
djangoRootPath = "${product_name}_djangoRootPath".format(product_name=product_name.lower())
djangoUwsgiPass = "${product_name}_djangoUwsgiPass".format(product_name=product_name.lower())
djangoStaticPath = "${product_name}_djangoStaticPath".format(product_name=product_name.lower())
djangoAdminStaticPath = "${product_name}_djangoAdminStaticPath".format(product_name=product_name.lower())
djangoMediaPath = "${product_name}_djangoMediaPath".format(product_name=product_name.lower())

DjangoNginxSetting = {

    djangoDomains : django_ip,
    djangoRootPath : path.join(subproject_path,"main/{project_name}".format(project_name=django_project_name)),
    djangoUwsgiPass : django_ip+":"+str(release_django_port),
    djangoStaticPath : static_path,
    djangoAdminStaticPath : path.join(static_path,"admin"),
    djangoMediaPath : media_path,
}

gfMakeDirs(DjangoNginxSetting[djangoMediaPath])
gfMakeDirs(DjangoNginxSetting[djangoRootPath])
