# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_schedule_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='swap',
            name='employee_1',
        ),
        migrations.RemoveField(
            model_name='swap',
            name='employee_2',
        ),
    ]
