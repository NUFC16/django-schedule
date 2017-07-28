# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0018_auto_20170728_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day_shift',
            name='time_from',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='day_shift',
            name='time_until',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
