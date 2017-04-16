# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20170414_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permanent_swap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField()),
                ('day_shift_1', models.ForeignKey(related_name='+', to='schedule.Day_shift')),
                ('day_shift_2', models.ForeignKey(related_name='+', to='schedule.Day_shift')),
                ('employee_1', models.ForeignKey(related_name='+', to='schedule.User')),
                ('employee_2', models.ForeignKey(related_name='+', to='schedule.User')),
            ],
        ),
    ]
