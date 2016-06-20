#-*- coding: UTF-8 -*-
__author__ = 'helios'

'''
    该类作为用户信息
'''

from Gyrfalcon.main.site.Account.GFUserReqHandlers import *
from Gyrfalcon.main.site.Account.GFUserSystems import *

class GFUserProfileReqHandler(GFUserReqHandler):

    def get(self,params):
        if not self.httpHeadersJson.has_key('userid') or self.httpHeadersJson['userid'] == "":
            # 请重新登录
            self.responseWrite(10008)
        else:
            queryList = [
                "username",
                "userid",
                "usignature",
                "expires_time",
                "deviceid",
                "email",
                "thumburl",
                "profileurl"
            ]
            condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
            userData = self.dbGet(queryList, condition)
            if len(userData) == 0:
                # 请求失败
                self.responseWrite(10004)
            elif userData['expires_time'] < time.time() or userData['deviceid'] != self.httpHeadersJson['deviceid'] or self.httpHeadersJson['usignature'] != userData['usignature']:
                # 请重新登录
                self.responseWrite(10008)
            else:
                del userData['deviceid']
                del userData['expires_time']
                # 请求成功
                self.responseWrite(0, "请求成功", userData)

class BMSetUsernameReqHandler(GFUserReqHandler):

    def get(self,params):

        if not self.httpHeadersJson.has_key('userid') or self.httpHeadersJson['userid'] == 0:
            # 请重新登录
            self.responseWrite(10008)
        else:
            queryList = [
                "username",
                "userid",
                "usignature",
                "expires_time",
                "deviceid",
                "email",
                "thumburl",
                "profileurl"
            ]
            condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
            userData = self.dbGet(queryList, condition)
            if userData['expires_time'] < time.time() or userData['deviceid'] != self.httpHeadersJson['deviceid'] or \
                self.httpHeadersJson['usignature'] != userData['usignature']:
                # 请重新登录
                self.responseWrite(10008)
            elif len(self.paramsJson['username']) > 16:
                # 用户名不能超过16个字
                self.responseWrite(10003)
            else:
                updateDict = {
                    "username":self.paramsJson["username"],
                }
                condition = "userid={userid}".format(userid=self.httpHeadersJson["userid"])
                flag = self.dbUpdate(updateDict, condition)
                if flag:
                    queryList = [
                        "username",
                        "userid",
                        "nickname",
                        "usignature",
                        "email",
                        "thumburl",
                        "profileurl"
                    ]
                    condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
                    userData = self.dbGet(queryList, condition)
                    self.responseWrite(0,"修改成功", userData)
                else:
                    # 修改失败
                    self.responseWrite(10005)

class BMSetNicknameReqHandler(GFUserReqHandler):

    def get(self,params):

        if not self.httpHeadersJson.has_key('userid'):
            # 请重新登录
            self.responseWrite(10008)
        else:
            queryList = [
                "username",
                "userid",
                "usignature",
                "expires_time",
                "deviceid",
                "email",
                "thumburl",
                "profileurl"
            ]
            condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
            userData = self.dbGet(queryList, condition)
            if userData['expires_time'] < time.time() or userData['deviceid'] != self.httpHeadersJson['deviceid'] or \
                self.httpHeadersJson['usignature'] != userData['usignature']:
                # 请重新登录
                self.responseWrite(10008)
            elif len(self.paramsJson['username']) > 20:
                # 昵称不能超过20个字
                self.responseWrite(10006)
            else:
                updateDict = {
                    "nickname":self.paramsJson["nickname"],
                }
                condition = "userid={userid}".format(userid=self.httpHeadersJson["userid"])
                flag = self.dbUpdate(updateDict, condition)
                if flag:
                    # 修改成功
                    queryList = [
                        "username",
                        "userid",
                        "nickname",
                        "usignature",
                        "email",
                        "thumburl",
                        "profileurl"
                    ]
                    condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
                    userData = self.dbGet(queryList, condition)
                    self.responseWrite(0, "修改成功", userData)
                else:
                    # 修改失败
                    self.responseWrite(10005)

class BMSetAvatarHandler(GFUserReqHandler):

    def post(self,params):
        img_type = ['image/jpeg', 'image/png']
        send_file = self.request.files['avatar'][0]
        if send_file['content_type'] not in img_type:
            # 图片格式不正确
            self.responseWrite(10011)
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=True)
            tmp_file.write(send_file['body'])
            tmp_file.seek(0)
            img = Image.open(tmp_file.name)
            img_path = "/home/pyweb/images/"
            img_name = send_file['filename'].split('.').pop().lower()
            tmp_name = img_path + BMCryptor.md5Password(time.time(),self.httpHeadersJson['userid']) + '.' +img_name
            img.save(tmp_name)
            tmp_file.close()
            updateList = {
                "thumburl":tmp_name
            }
            condition = "userid={userid}".format(userid=self.httpHeadersJson["userid"])
            flag = self.dbUpdate(updateList, condition)
            if flag:
                # 修改成功
                queryList = [
                    "username",
                    "userid",
                    "nickname",
                    "usignature",
                    "email",
                    "thumburl",
                    "profileurl"
                ]
                condition = "userid={userid}".format(userid=int(self.httpHeadersJson['userid']))
                userData = self.dbGet(queryList, condition)
                # 修改成功
                self.responseWrite(0, "修改成功", userData)
            else:
                # 修改失败
                self.responseWrite(10005)
