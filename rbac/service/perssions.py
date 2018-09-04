# -*- coding: utf-8 -*-
# @Time    : 2018/08/11 0011 9:24
# @Author  : Venicid


def initial_session(request,user):
    # 方案2
    permissions = user.roles.all().values("permissions__url", "permissions__group_id","permissions__action").distinct()
    print(permissions)
    # <QuerySet [{'permissions__url': '/users/',
                # 'permissions__group_id': 1,
                # 'permissions__action': 'list'}]>

    permission_dict = {}
    for item in permissions:
        gid = item.get("permissions__group_id")
        if not gid in permission_dict:
            permission_dict[gid] = {
                "urls":[item["permissions__url"],],
                "actions":[item["permissions__action"],]
            }
        else:
            permission_dict[gid]["urls"].append(item["permissions__url"])
            permission_dict[gid]["actions"].append(item["permissions__action"])

    print(permission_dict)  # {1: {'urls': ['/users/'], 'actions': ['list']}}
    request.session["permission_dict"] = permission_dict


    # 注册菜单权限
    # permissions = user.roles.all().values("permissions__url", "permissions__action", "permissions__group__title").distinct()
    permissions = user.roles.all().values("permissions__url", "permissions__action", "permissions__title").distinct()

    # print(permissions)
    menu_permission_list = []
    for item in permissions:
        if item["permissions__action"] == "list":
            print(item)
            # menu_permission_list.append((item["permissions__url"], item["permissions__group__title"]))  # 组的名称
            menu_permission_list.append((item["permissions__url"], item["permissions__title"]))
           # 用自己permission的title

    # print(menu_permission_list)   # [('/users/', '用户组'), ('/roles/', '角色组')]
    request.session["menu_permission_list"] = menu_permission_list


    # 方案1：
    """
    permissions = user.roles.all().values("permissions__url").distinct()

    permission_list = []
    for item in permissions:
        permission_list.append(item['permissions__url'])

    print(permission_list)  # ['/users/', '/users/add', '/users/delete/(\\d+)', '/users/edit/(\\d+)']

    request.session["permission_list"] = permission_list
    """

    """
    values :

    for role in user.roles.all():   # <QuerySet [<Role: 保洁>, <Role: 销售>]>
        temp.append({
        "title":role.title,
        "permissions_url":role.permissions.all()
        })

    # <QuerySet [{'title': '保洁', 'permissions__url': '/users/'},
    # {'title': '销售', 'permissions__url': '/users/'},
    # {'title': '销售', 'permissions__url': '/users/add'}]>

    """