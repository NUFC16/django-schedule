# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0023_auto_20170807_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='default_wage',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2, blank=True),
        ),
    ]
