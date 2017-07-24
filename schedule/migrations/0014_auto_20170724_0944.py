# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20170724_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='last_name',
        ),
    ]
