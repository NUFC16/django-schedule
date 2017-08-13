# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0025_swap_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
