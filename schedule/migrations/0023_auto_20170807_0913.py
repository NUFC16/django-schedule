# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0022_auto_20170804_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='date_of_employment',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', 'Male'), (b'F', 'Female')]),
        ),
    ]
