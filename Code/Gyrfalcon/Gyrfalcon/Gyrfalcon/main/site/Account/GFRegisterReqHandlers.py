#-*- coding: UTF-8 -*-
__author__ = 'helios'

'''
    该类作为用户注册
'''
from Gyrfalcon.main.site.Account.GFUserReqHandlers import *

class BMRegisterReqHandler(GFUserReqHandler):

    def get(self,params):
        gflog("paramsJson:"+str(self.paramsJson))
        if len(self.paramsJson) == 0:
            # 请求错误
            self.responseWrite(10014)
        else:
            if len(self.paramsJson.get("email")) == 0 or len(self.paramsJson['password']) == 0:
                # 邮箱或密码不能为空
                self.responseWrite(10012)
            else:
                pattern = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
                match = pattern.match(self.paramsJson['email'])
                if not match:
                    # 邮箱格式不正确
                    self.responseWrite(10017)
                else:
                    existUsers = GFUser.objects.filter(email=self.paramsJson["email"])
                    gflog("register"+str(self.paramsJson))
                    if len(existUsers) > 0:
                        # 邮箱已被注册，请更换邮箱注册
                        self.responseWrite(10010)
                    else:
                        try:
                            user = GFUser.objects.create(username=self.paramsJson["email"],email=self.paramsJson["email"],password=self.paramsJson["password"])
                            user.userid = identifierAuto()
                            user.nickname = self.paramsJson["email"]
                            respUserDict = {
                                "username":user.username,
                                "password":user.password,
                                "usignature":user.usignature,
                                "email":user.email,
                                "register_time":str(user.date_of_birth),
                                "deviceid":user.deviceid,
                                "devicetoken":user.devicetoken,
                                "userid":user.userid,
                                "nickname":user.nickname,
                                "thumburl":user.thumb.path
                            }

                            self.responseWrite(0,"注册成功",respUserDict)
                        except Exception as e:
                            gflog(str(e));
                            if e == GFUser.DoesNotExist:
                                # 邮箱已被注册，请更换邮箱注册
                                self.responseWrite(10010)
                            else:
                                # 注册失败
                                self.responseWrite(10015)
