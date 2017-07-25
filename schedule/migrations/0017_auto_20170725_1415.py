# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0016_auto_20170724_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='user_group',
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user_group',
            field=models.ManyToManyField(to='schedule.Group', null=True),
        ),
    ]
