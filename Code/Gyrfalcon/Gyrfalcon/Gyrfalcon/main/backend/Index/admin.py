#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

from django.contrib import admin
from Index import models

class IndexAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.IndexModel,IndexAdmin)
# Register your models here.
