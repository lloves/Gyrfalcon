#-*- coding: UTF-8 -*-
__author__ = 'helios'

'''
    该类作为用户注册
'''

from Account.models import GFUser
from Gyrfalcon.main.site.Common.GFAPIReqHandlers import *
from Gyrfalcon.main.site.Account.GFUserSystems import GFUserSystem

class GFUserReqHandler(GFAPIReqHandler):

    #  @def current_user():
    #
    #      doc = "The current_user property."
    #      def fget(self):
    #          return self._current_user
    #      def fset(self, value):
    #          self._current_user = value
    #      def fdel(self):
    #          del self._current_user
    #      return locals()

    # current_user = property(**current_user())

    def get(self, *args, **kwargs):
        self.write()
