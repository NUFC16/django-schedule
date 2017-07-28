# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20170725_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='week_shift',
            name='name',
            field=models.CharField(default='bzvz', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='user_group',
            field=models.ManyToManyField(to='schedule.Group'),
        ),
    ]
