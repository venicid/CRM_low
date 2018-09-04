# -*- coding: utf-8 -*-
# @Time    : 2018/09/04 0004 9:26
# @Author  : Venicid
from stark.service.stark import site,ModelStark

from .models import *

class UserConfig(ModelStark):
    list_display = ['name','roles']

site.register(User,UserConfig)
site.register(Role)

class PermissionConfig(ModelStark):


    list_display = ['id','title','url','group','action']

site.register(Permission,PermissionConfig)
site.register(PermissionGroup)
