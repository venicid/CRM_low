# Generated by Django 2.0.1 on 2018-08-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_remove_permission_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='action',
            field=models.CharField(default='', max_length=32),
        ),
    ]