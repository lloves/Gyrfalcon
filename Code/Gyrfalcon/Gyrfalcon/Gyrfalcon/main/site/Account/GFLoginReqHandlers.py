#-*- coding: UTF-8 -*-
__author__ = 'helios'

'''
    该类作为用户登录
'''

from Gyrfalcon.main.site.Account.GFUserReqHandlers import *

class BMLoginReqHandler(GFUserReqHandler):

    def get(self, params):
        gflog(self.httpHeadersJson)
        if len(self.paramsJson) == 0 or len(self.httpHeadersJson) == 0:
	        # 请求错误
            self.responseWrite(10014)
        else:
            if len(self.paramsJson['username']) == 0 or len(self.paramsJson['password']) == 0:
                # 邮箱或密码不能为空
                self.responseWrite(10012)
            else:
                pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
                match = pattern.match(self.paramsJson['username'])

                if match:
                    # 邮箱登录
                    users = GFUser.objects.filter(email = self.paramsJson['username'])
                    gflog("login:"+str(self.paramsJson))
                    if len(users) > 0:
                        # 邮箱存在，开始验证密码
                        user = users[0]

                        if user.password == self.paramsJson["password"]:
                            # 登录成功
                            respUserDict = {
                                "username":user.username,
                                "password":user.password,
                                "usignature":user.usignature,
                                "email":user.email,
                                "register_time":str(user.date_of_birth),
                                "deviceid":user.deviceid,
                                "devicetoken":user.devicetoken,
                                "userid":user.userid,
                                "nickname":user.nickname
                            }

                            self.responseWrite(0, "登录成功", respUserDict)
                        else:
                            # 密码或者用户名错误
                            self.responseWrite(10002)
                    else:
                        # 用户不存在， 注册加入我们吧~~~
                        self.responseWrite(10016)
                else:
                    # 用户名登录
                    users = GFUser.objects.filter(username = self.paramsJson['username'])
                    if len(users) > 0:
                        user = users[0]
                        if user.password == self.paramsJson["password"]:
                            # 登录成功
                            respUserDict = {
                                "username":user.username,
                                "password":user.password,
                                "usignature":user.usignature,
                                "email":user.email,
                                "register_time":str(user.date_of_birth),
                                "deviceid":user.deviceid,
                                "devicetoken":user.devicetoken,
                                "userid":user.userid,
                            }
                            self.responseWrite(0, "登录成功", respUserDict)
                        else:
                            # 密码或者用户名错误
                            self.responseWrite(10002)
                    else:
                        # 用户不存在， 注册加入我们吧~~~
                        self.responseWrite(10016)

class BMLogoutReqHandler(GFUserReqHandler):

    def get(self):
        users = GFUser.objects.filter(userid=self.httpHeadersJson['userid'])
        if len(users) > 0:
            for user in users:
                user.usginature=str(uuid.uuid3(uuid.uuid4(),str(time.time())).hex)
                user.expires_time=datetime.datetime.now()+datetime.timedelta(days=-365*5)
                user.save()
            self.responseWrite(0, "注销成功", {})
        else:
            # 注销失败
            self.responseWrite(0, "注销成功", {})
