# -*- coding: utf-8 -*-
# @Time    : 2018/08/12 0012 16:11
# @Author  : Venicid

from django import template

register = template.Library()


@register.inclusion_tag("rbac/menu.html")
def get_menu(request):
    # 获取当前用户可以放到菜单栏中的权限
    menu_permission_list = request.session.get("menu_permission_list")

    print(menu_permission_list)

    return {"menu_permission_list":menu_permission_list}