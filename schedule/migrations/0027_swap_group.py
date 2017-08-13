# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0026_swap_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='group',
            field=models.ForeignKey(to='schedule.Group', null=True),
        ),
    ]
