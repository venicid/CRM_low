from django.db import models


# Create your models here.




class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to="Permission")

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    roles = models.ManyToManyField(to='Role')

    def __str__(self):
        return self.name


class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=1024)
    action = models.CharField(max_length=32, default="")

    group = models.ForeignKey(to="PermissionGroup", on_delete=True)
    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
     title = models.CharField(max_length=32 )
     def __str__(self):
         return self.title