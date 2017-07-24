# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0015_auto_20170724_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='supervisor',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
