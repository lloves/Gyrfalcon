#-*- coding: UTF-8 -*-
__author__ = 'helios'

from Gyrfalcon.Globals import *
from Gyrfalcon.tools.database.DBSession import DBSession
from Gyrfalcon.configure.GlobalConfigure import template_path, static_path
from Gyrfalcon.tools.results.ResultAsistances import ResultAsistance
from django.db import connection, connections

class GFReqHandler(tornado.web.RequestHandler):
    static_path = static_path
    template_path = template_path
    tableName = ""
    session = DBSession()

    def __init__(self, application, request, **kwargs):
        super(GFReqHandler, self).__init__(application, request)
        self.tableName = ""

    def on_finish(self, *args, **kargs):
        self.session.close()
        for c in connections.all():
            try:
                c._commit()
            except:
                pass

        if connection.connection and not connection.is_usable():
            # destroy the default mysql connection
            # after this line, when you use ORM methods
            # django will reconnect to the default mysql
            del connections._connections.default

        return

    def prepare(self):

        if connection.connection and not connection.is_usable():
            # destroy the default mysql connection

            # after this line, when you use ORM methods
            # django will reconnect to the default mysql
            del connections._connections.default


        for c in connections.all():
            try:
                c._commit()
            except:
                pass

        return

#数据库操作
    def dbGet(self, items, condition):
        return self.session.get(self.tableName, items, condition)

    def dbInsert(self, params):
        return self.session.insert(self.tableName, params)

    def dbUpdate(self, params, condition):
        return self.session.update(self.tableName, params, condition)

    @property
    def params(self):
        if self.get_argument('params') == None:
            return ""
        return self.get_argument('params')

    @property
    def paramsJson(self):

        try:
            if desText.__len__() == 0:
                return {}
            else:
                return json.loads(self.params)

        except:
            return {}

    def responseWrite(self,code=0, message="", data={}):
        self.write(GFReqHandler.responseDataText(code, message, data))

    def responseDataText(code=0, message="", data={}):

        responseData = ResultAsistance.resultErrorDataWrapperToJson(code,data)
        if code == 0:
            responseData = ResultAsistance.resultSuccessDataWrapperToJson(message, data)

        responseDataText = json.dumps(responseData)
        return responseDataText
