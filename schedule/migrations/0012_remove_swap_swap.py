# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_auto_20170513_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='swap',
            name='swap',
        ),
    ]
