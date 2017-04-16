# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day_shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_from', models.TimeField()),
                ('time_until', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time_from', models.TimeField()),
                ('time_until', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Swap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('status', models.BooleanField()),
                ('day_shift_1', models.ForeignKey(related_name='+', to='schedule.Day_shift')),
                ('day_shift_2', models.ForeignKey(related_name='+', to='schedule.Day_shift')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('user_group', models.ForeignKey(to='schedule.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week_shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('monday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('saturday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('sunday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('thuesday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('thursday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('wednesday', models.ForeignKey(related_name='+', to='schedule.Day_shift', null=True)),
                ('week_group', models.ForeignKey(to='schedule.Group')),
            ],
        ),
        migrations.AddField(
            model_name='swap',
            name='employee_1',
            field=models.ForeignKey(related_name='+', to='schedule.User'),
        ),
        migrations.AddField(
            model_name='swap',
            name='employee_2',
            field=models.ForeignKey(related_name='+', to='schedule.User'),
        ),
        migrations.AddField(
            model_name='swap',
            name='schedule_1',
            field=models.ForeignKey(related_name='+', to='schedule.Schedule'),
        ),
        migrations.AddField(
            model_name='swap',
            name='schedule_2',
            field=models.ForeignKey(related_name='+', to='schedule.Schedule'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(to='schedule.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='supervisor',
            field=models.ForeignKey(to='schedule.Staff'),
        ),
    ]
