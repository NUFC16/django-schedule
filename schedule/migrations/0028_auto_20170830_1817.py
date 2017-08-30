# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0027_swap_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swap',
            name='group',
            field=models.ForeignKey(to='schedule.Group'),
        ),
        migrations.AlterField(
            model_name='swap',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='Date of birth', blank=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='date_of_employment',
            field=models.DateField(null=True, verbose_name='Date of employment', blank=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='default_wage',
            field=models.DecimalField(default=0, verbose_name='Default wage', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Gender', choices=[(b'M', 'Male'), (b'F', 'Female')]),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='user_groups',
            field=models.ManyToManyField(to='schedule.Group', verbose_name='User groups'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='user_shift',
            field=models.ForeignKey(verbose_name='Week shift', to='schedule.Week_shift', null=True),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Shift name'),
        ),
        migrations.AlterField(
            model_name='week_shift',
            name='week_group',
            field=models.ForeignKey(verbose_name='Week group', to='schedule.Group'),
        ),
    ]
