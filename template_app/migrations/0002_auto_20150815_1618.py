# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User


def forwards_func(apps, schema_editor):
    ''' add an admin user '''
    user = User(pk=1, username="admin", is_active=True,
                is_superuser=True, is_staff=True,
                last_login="2011-09-01T13:20:30+03:00",
                email="test@test.com",
                date_joined="2011-09-01T13:20:30+03:00")
    user.set_password('admin')
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('template_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop)
    ]
