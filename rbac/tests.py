from django.test import TestCase

# Create your tests here.

li = [

    {'permissions__url': '/users/add/',
     'permissions__group_id': 1,
     'permissions__action': 'add'},

    {'permissions__url': '/roles/',
     'permissions__group_id': 2,
     'permissions__action': 'list'},

    {'permissions__url': '/users/delete/(\\d+)',
     'permissions__group_id': 1,
     'permissions__action': 'delete'},

    {'permissions__url': 'users/edit/(\\d+)',
     'permissions__group_id': 1,
     'permissions__action': 'edit'}
]




"""
dict ={1:{"urls":[], "actions":[]},2:{"urls":[], "actions":[]}}
for item in li:
    if item["permissions__group_id"] == 1:
        dict[1]['urls'].append(item["permissions__url"])
        dict[1]['actions'].append(item["permissions__action"])

    if item["permissions__group_id"] == 2:
        dict[2]['urls'].append(item["permissions__url"])
        dict[2]['actions'].append(item["permissions__action"])
print(dict)
"""



class Person(object):
    def __init__(self,name):
        self.name = name

alex = Person("alex")
print(alex.name)

alex.age = 33
alex.actions = 'list'
print(alex.__dict__)
