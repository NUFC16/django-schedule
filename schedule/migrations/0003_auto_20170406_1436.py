# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_user_user_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time_from',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_until',
            field=models.TimeField(null=True),
        ),
    ]
