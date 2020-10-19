# Generated by Django 3.1.2 on 2020-10-19 10:08

from django.db import migrations

from users import permissions, roles


def create_permissions(apps, _):
    Permission = apps.get_model('users', 'Permission')
    Role = apps.get_model('users', 'Role')
    permission = Permission.objects.create(codename=permissions.CAN_CREATE_CLIENT_APPLICATION)

    role = Role.objects.get(codename=roles.PARTNER['codename'])
    role.permissions.add(permission)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_auto_20201019_0738'),
    ]

    operations = [
        migrations.RunPython(create_permissions)
    ]