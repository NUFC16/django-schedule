# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_auto_20170513_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permanent_swap',
            name='day_shift_1',
        ),
        migrations.RemoveField(
            model_name='permanent_swap',
            name='day_shift_2',
        ),
        migrations.RemoveField(
            model_name='permanent_swap',
            name='employee_1',
        ),
        migrations.RemoveField(
            model_name='permanent_swap',
            name='employee_2',
        ),
        migrations.AddField(
            model_name='swap',
            name='permanent',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Permanent_swap',
        ),
    ]
