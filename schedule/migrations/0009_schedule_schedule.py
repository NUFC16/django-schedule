# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_swap_swap'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule',
            field=models.ForeignKey(related_name='+', verbose_name='Parent schedule', blank=True, to='schedule.Schedule', null=True),
        ),
    ]
