#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class IndexModel(models.Model):

    class Meta:
        verbose_name = _(u"首页")
        verbose_name_plural = _(u"首页")
        db_table = _(u"index_indexmodel")

    # def __str__(self):
    #     return str(self.createUser.username)+"."+self.Index.text
