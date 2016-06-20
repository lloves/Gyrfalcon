#-*- coding: UTF-8 -*-
__author__ = 'helios'
'''
    该类作为接口测试
'''

from Gyrfalcon.main.site.Common.GFAPIReqHandlers import *
from Gyrfalcon.main.site.Common.GFWebReqHandlers import *


class GFIndexReqHandler(GFWebReqHandler):
	"""docstring for GFIndexReqHandler"""

	def get(self):
		return self.render("index/index.html", title="Test")

		