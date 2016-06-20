#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

from Gyrfalcon.main.site.Index.GFIndexReqHandlers import GFIndexReqHandler

version = 1.0

def GFApiPathURL(channel, path, className):
    return (r"/api/{version}/{channel}/{path}".format(version=version, channel=channel, path=path), className)

# url配置信息
apiList = [

]

webList = [

    # 首页
    (r"/", GFIndexReqHandler),

]

urlList = apiList+webList
