# -*- coding: utf-8 -*-
# @Time    : 2018/08/11 0011 9:04
# @Author  : Venicid

import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class ValidPermission(MiddlewareMixin):
    def process_request(self, request):

        # 当前访问路径
        current_path = request.path_info

        # 1、检验是否属于白名单  白名单，不需要任何权限的url
        # 正则匹配
        valid_url_list = ['/login/', '/reg/', '/admin/.*']
        for valid_url in valid_url_list:
            ret = re.match(valid_url, current_path)

            if ret:
                return None

        # 2、校验是否登录
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect('/login/')

        # 3、校验权限2

        permission_dict = request.session.get("permission_dict", {})
        # {1: {'urls': ['/users/'], 'actions': ['list']}}

        for item in permission_dict.values():
            urls = item["urls"]
            for reg in urls:
                reg = "^%s$" % reg
                ret = re.match(reg, current_path)
                if ret:
                    print("actions",item["actions"])
                    request.actions = item["actions"]
                    return None
        return HttpResponse("没有访问权限")

        # 3、校验权限1
        """
        permission_list = request.session.get("permission_list",[])
        print(permission_list)

        flag = False
        for permission in permission_list:
            permission = "^%s$" % permission
            # print(111111111,permission)
            # print(current_path)
            ret = re.match(permission, current_path)
            if ret:
                flag = True
                break

        if not flag:
            return HttpResponse("没有访问权限")
        return None
        """
