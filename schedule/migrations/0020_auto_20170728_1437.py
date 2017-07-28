# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0019_auto_20170728_0757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_profile',
            old_name='user_group',
            new_name='user_groups',
        ),
    ]
