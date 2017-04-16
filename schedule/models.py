from django.db import models
from django import forms

import datetime


class Staff(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # password = models.CharField(widget=forms.PasswordInput)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Group(models.Model):
    group_name = models.CharField(max_length=30)
    supervisor = models.ForeignKey(Staff)

    def __unicode__(self):
        return self.group_name


class Day_shift(models.Model):
    time_from = models.TimeField()
    time_until = models.TimeField()

    def __unicode__(self):
        return 'Day_shift ' + str(self.time_from.hour) + '-' + str(self.time_until.hour)


class Week_shift(models.Model):
    monday = models.ForeignKey(Day_shift, null=True, related_name='+')
    thuesday = models.ForeignKey(Day_shift, null=True, related_name='+')
    wednesday = models.ForeignKey(Day_shift, null=True, related_name='+')
    thursday = models.ForeignKey(Day_shift, null=True, related_name='+')
    friday = models.ForeignKey(Day_shift, null=True, related_name='+')
    saturday = models.ForeignKey(Day_shift, null=True, related_name='+')
    sunday = models.ForeignKey(Day_shift, null=True, related_name='+')
    week_group = models.ForeignKey(Group)

    def __unicode__(self):
        return 'Week_shift ' + self.week_group.group_name + ' ' + str(self.id)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # password = models.CharField(widget=forms.PasswordInput)
    user_group = models.ForeignKey(Group, null=True)
    user_shift = models.ForeignKey(Week_shift, null=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Schedule(models.Model):
    date = models.DateField()
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(User)

    def switch_case(self, x):
        return {
            0: self.user.user_shift.monday,
            1: self.user.user_shift.thuesday,
            2: self.user.user_shift.wednesday,
            3: self.user.user_shift.thursday,
            4: self.user.user_shift.friday,
            5: self.user.user_shift.saturday,
            6: self.user.user_shift.sunday,
        }.get(x, 6)

    def save(self, *args, **kwargs):
        if (self.time_from == None or self.time_until == None):
            temp_shift = self.switch_case(self.date.weekday())

            self.time_from = temp_shift.time_from
            self.time_until = temp_shift.time_until
        # Call the "real" save() method.
        super(Schedule, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Schedule ' + self.date.strftime('%m/%d/%Y') + ' ' + self.user.first_name + ' ' + self.user.last_name


class Swap(models.Model):
    employee_1 = models.ForeignKey(User, related_name='+')
    employee_2 = models.ForeignKey(User, related_name='+')
    schedule_1 = models.ForeignKey(Schedule, related_name='+')
    schedule_2 = models.ForeignKey(Schedule, related_name='+')
    date = models.DateField()
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        swp1 = Schedule.objects.get(pk=self.schedule_1.pk)
        swp1.user = self.employee_2
        swp1.save()
        swp2 = Schedule.objects.get(pk=self.schedule_2.pk)
        swp2.user = self.employee_1
        swp2.save()
        super(Swap, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Swap ' + self.date.strftime('%m/%d/%Y') + ' ' + str(self.id)


class Permanent_swap(models.Model):
    employee_1 = models.ForeignKey(User, related_name='+')
    employee_2 = models.ForeignKey(User, related_name='+')
    day_shift_1 = models.ForeignKey(Day_shift, related_name='+')
    day_shift_2 = models.ForeignKey(Day_shift, related_name='+')
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Permanent swap ' + self.date.strftime('%m/%d/%Y') + ' ' + str(self.id)
