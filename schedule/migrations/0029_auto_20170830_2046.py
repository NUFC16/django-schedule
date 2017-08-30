# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0028_auto_20170830_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='receiver_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='week_group',
            field=models.ForeignKey(verbose_name='Group', to='schedule.Group'),
        ),
    ]
