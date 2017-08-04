# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0020_auto_20170728_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week_shift',
            name='friday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='monday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='saturday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='sunday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='thuesday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='thursday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='wednesday',
            field=models.ForeignKey(related_name='+', blank=True, to='schedule.Day_shift', null=True),
        ),
    ]
