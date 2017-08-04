# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0021_auto_20170803_0930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='week_shift',
            old_name='thuesday',
            new_name='tuesday',
        ),
    ]
