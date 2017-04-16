# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20170406_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='swap',
            name='day_shift_1',
        ),
        migrations.RemoveField(
            model_name='swap',
            name='day_shift_2',
        ),
        migrations.RemoveField(
            model_name='swap',
            name='status',
        ),
    ]
