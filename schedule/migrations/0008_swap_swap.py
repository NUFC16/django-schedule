# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20170414_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='swap',
            field=models.ForeignKey(related_name='+', verbose_name='Parent swap', blank=True, to='schedule.Swap', null=True),
        ),
    ]
