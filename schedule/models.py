from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
from django.utils.translation import ugettext_lazy as _

import datetime


class Group(models.Model):
    group_name = models.CharField(max_length=30)
    supervisor = models.ForeignKey(User, related_name='+',)

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if hasattr(self, 'supervisor'):
            self.old_supervisor = self.supervisor

    def get_members():
        return self.user_profile_set.all()

    def __unicode__(self):
        return self.group_name


class Day_shift(models.Model):
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return 'Day_shift ' + str(self.time_from.hour) + '-' + str(self.time_until.hour)


class Week_shift(models.Model):
    name = models.CharField(max_length=30)
    monday = models.ForeignKey(Day_shift, null=True, related_name='+')
    thuesday = models.ForeignKey(Day_shift, null=True, related_name='+')
    wednesday = models.ForeignKey(Day_shift, null=True, related_name='+')
    thursday = models.ForeignKey(Day_shift, null=True, related_name='+')
    friday = models.ForeignKey(Day_shift, null=True, related_name='+')
    saturday = models.ForeignKey(Day_shift, null=True, related_name='+')
    sunday = models.ForeignKey(Day_shift, null=True, related_name='+')
    week_group = models.ForeignKey(Group)

    def get_day(self, x):
        return {
            0: self.monday,
            1: self.thuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }.get(x, 6)

    def change_day(self, x, val):
        if x == 0:
            self.monday = val
        elif x == 1:
            self.thuesday = val
        elif x == 2:
            self.wednesday = val
        elif x == 3:
            self.thursday = val
        elif x == 4:
            self.friday = val
        elif x == 5:
            self.saturday = val
        elif x == 6:
            self.sunday = val

    def __unicode__(self):
        return self.name


class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_groups = models.ManyToManyField(Group)
    user_shift = models.ForeignKey(Week_shift, null=True)

    def generate_schedule(self):
        a = datetime.datetime.today()
        numdays = 60
        for x in range(0, numdays):
            date = a + datetime.timedelta(days=x)
            try:
                Schedule.objects.get(date=date, user=self)
            except:
                Schedule.objects.create(date=date, user=self)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=Group)
def update_supervisor(sender, instance, created, **kwargs):
    # if instance is created
    if instance:
        try:
            new_supervisor = User_profile.objects.get(user=instance.supervisor)
        except:
            return
        new_supervisor.user_groups.add(instance)
        new_supervisor.save()

        try:
            old_supervisor = User_profile.objects.get(
                user=instance.old_supervisor)
        except:
            return
        old_supervisor.user_groups.remove(instance)
        old_supervisor.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_profile.user_shift:
        instance.user_profile.save()


@receiver(models.signals.post_save, sender=User_profile)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if not created:
        instance.generate_schedule()


class Schedule(models.Model):
    schedule = models.ForeignKey(
        "self",
        related_name='+',
        verbose_name=_('Parent schedule'),
        null=True,
        blank=True
    )
    date = models.DateField()
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(User_profile)

    def save(self, make_instance=False, *args, **kwargs):
        if self.time_from == None or self.time_until == None:
            temp_shift = self.user.user_shift.get_day(self.date.weekday())

            self.time_from = temp_shift.time_from
            self.time_until = temp_shift.time_until

        if make_instance == True:
            # In case of change - followup
            try:
                new_followup = Schedule.objects.get(pk=self.pk)
                new_followup.pk = None
                new_followup.schedule = self
                new_followup.save()
            except:
                pass
        # Call the "real" save() method.
        super(Schedule, self).save(*args, **kwargs)

    def get_string_from(self):
        return self.date.strftime('%Y-%m-%d') + 'T' + self.time_from.strftime('%H:%M:%S')

    def get_string_until(self):
        return self.date.strftime('%Y-%m-%d') + 'T' + self.time_until.strftime('%H:%M:%S')

    def __unicode__(self):
        return 'Schedule ' + self.date.strftime('%m/%d/%Y') + ' ' + self.user.user.first_name + ' ' + self.user.user.last_name


class Swap(models.Model):
    schedule_1 = models.ForeignKey(Schedule, related_name='+')
    schedule_2 = models.ForeignKey(Schedule, related_name='+')
    date = models.DateField()
    permanent = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def revert(self):
        self.save(make_instance=False)
        self.delete()

    def save(self, make_instance=True, *args, **kwargs):
        # Swap schedules(class) which enables change to be visible in real
        # schedule
        sch_1 = Schedule.objects.get(pk=self.schedule_1.pk)
        sch_2 = Schedule.objects.get(pk=self.schedule_2.pk)

        if self.permanent == True:
            shift_1 = sch_1.user.user_shift
            shift_2 = sch_2.user.user_shift

            day_1 = shift_1.get_day(sch_1.date.weekday())
            day_2 = shift_2.get_day(sch_2.date.weekday())

            shift_1.change_day(sch_1.date.weekday(), day_2)
            shift_1.save()
            shift_2.change_day(sch_2.date.weekday(), day_1)
            shift_2.save()

        sch_1.user, sch_2.user = sch_2.user, sch_1.user
        sch_1.save(make_instance=make_instance)
        sch_2.save(make_instance=make_instance)
        # save current stati if reverse is used
        if make_instance == False:
            follow_schedule_1 = Schedule.objects.get(schedule=sch_1)
            follow_schedule_2 = Schedule.objects.get(schedule=sch_2)
            follow_schedule_1.delete()
            follow_schedule_2.delete()

        super(Swap, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Swap ' + self.date.strftime('%m/%d/%Y') + ' ' + str(self.id)
