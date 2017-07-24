# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0012_remove_swap_swap'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_group',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_shift',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(to='schedule.User_profile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user_group',
            field=models.ForeignKey(to='schedule.Group', null=True),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user_shift',
            field=models.ForeignKey(to='schedule.Week_shift', null=True),
        ),
    ]
