# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_permanent_swap'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='permanent_swap',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
