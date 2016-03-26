# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User
from django.utils import timezone


def forwards_func(apps, schema_editor):
    ''' add an admin user '''
    user = User(pk=1, username="admin", is_active=True,
                is_superuser=True, is_staff=True,
                last_login=timezone.now(),
                email="test@test.com",
                date_joined=timezone.now())
    user.set_password('admin')
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('template_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop)
    ]
