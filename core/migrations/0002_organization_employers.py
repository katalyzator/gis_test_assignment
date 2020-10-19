# Generated by Django 3.1.2 on 2020-10-19 16:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='employers',
            field=models.ManyToManyField(related_name='organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]
