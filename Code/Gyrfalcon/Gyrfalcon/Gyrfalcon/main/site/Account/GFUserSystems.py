#-*- coding: UTF-8 -*-
__author__ = 'helios'

'''
    该类作为用户系统帮助工具
'''

import uuid, time
from Gyrfalcon.tools.database.DBSession import DBSession

class GFUserSystem:

    session = DBSession()

    def __init__(self):
        self.tableName = "Gyrfalcon_usersystem"

    #单例设计模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(GFUserSystem,cls).__new__(cls,*args,**kwargs)
        return cls._inst

    def validateInfo(self, condition):

        queryList = ["userid"]
        rows = self.session.get(self.tableName, queryList, condition)
        if len(rows) > 0:
            return True
        else:
            return False

    def validateUsername(self,username):

        condition = "username='{username}'".format(username=username)
        return self.validateInfo(condition)

    def validateEmail(self,email):

        condition = "email='{email}'".format(email=email)
        return self.validateInfo(condition)
