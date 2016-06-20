#-*- coding: UTF-8 -*-

import sys
from os import path

#将项目模块加入全局模块路径中
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(0, path.realpath(BASE_DIR))

from Globals import *
djangoload()
import tornado
from service.Services import Service

# 应用启动配置
if __name__ == "__main__":
    
    Service().start()
