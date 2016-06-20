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

djangoDomains = "$djangoDomains"
djangoRootPath = "$djangoRootPath"
djangoUwsgiPass = "$djangoUwsgiPass"
djangoStaticPath = "$djangoStaticPath"
djangoAdminStaticPath = "$djangoAdminStaticPath"
djangoMediaPath = "$djangoMediaPath"

DjangoNginxSetting = {

    djangoDomains : "localhost",
    djangoRootPath : path.join(subproject_path,"main/{project_name}".format(project_name=django_project_name)),
    djangoUwsgiPass : "127.0.0.1:"+str(release_django_port),
    djangoStaticPath : static_path,
    djangoAdminStaticPath : path.join(static_path,"admin"),
    djangoMediaPath : media_path,
}

gfMakeDirs(DjangoNginxSetting[djangoMediaPath])
gfMakeDirs(DjangoNginxSetting[djangoRootPath])
