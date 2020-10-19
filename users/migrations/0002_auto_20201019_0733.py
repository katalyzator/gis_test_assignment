# Generated by Django 3.1.2 on 2020-10-19 07:33

from django.db import migrations

from users import permissions, roles


def create_permissions(apps, _):
    Permission = apps.get_model('users', 'Permission')
    Permission.objects.create(codename=permissions.CAN_DO_ANYTHING)


def create_role(apps, _):
    Role = apps.get_model('users', 'Role')

    administrator = Role.objects.create(codename=roles.ADMINISTRATOR['codename'],
                                        ru_name=roles.ADMINISTRATOR['ru_name'])
    administrator.permissions.add(
        permissions.CAN_DO_ANYTHING
    )

    Role.objects.create(codename=roles.PARTNER['codename'],
                        ru_name=roles.PARTNER['ru_name'])

    Role.objects.create(codename=roles.ORGANIZATION_SPECIALIST['codename'],
                        ru_name=roles.ORGANIZATION_SPECIALIST['ru_name'])


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permissions),
        migrations.RunPython(create_role),
    ]
