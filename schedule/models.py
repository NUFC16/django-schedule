from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

import datetime


class Group(models.Model):
    group_name = models.CharField(max_length=30)
    supervisor = models.ForeignKey(User, related_name='+',)

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if hasattr(self, 'supervisor'):
            self.old_supervisor = self.supervisor

    def get_members(self):
        return self.user_profile_set.all()

    def __unicode__(self):
        return self.group_name


class Day_shift(models.Model):
    time_from = models.TimeField(null=True, blank=True)
    time_until = models.TimeField(null=True, blank=True)

    def __unicode__(self):
        return 'Day_shift ' + str(self.time_from) + '-' + str(self.time_until)


class Week_shift(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Shift name'))
    monday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    tuesday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    wednesday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    thursday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    friday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    saturday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    sunday = models.ForeignKey(
        Day_shift, null=True, blank=True, related_name='+')
    week_group = models.ForeignKey(Group, verbose_name=_('Group'))

    def save(self, *args, **kwargs):
        if self.monday == None:
            self.monday = Day_shift.objects.create()
        if self.tuesday == None:
            self.tuesday = Day_shift.objects.create()
        if self.wednesday == None:
            self.wednesday = Day_shift.objects.create()
        if self.thursday == None:
            self.thursday = Day_shift.objects.create()
        if self.friday == None:
            self.friday = Day_shift.objects.create()
        if self.saturday == None:
            self.saturday = Day_shift.objects.create()
        if self.sunday == None:
            self.sunday = Day_shift.objects.create()

        super(Week_shift, self).save(*args, **kwargs)

    def get_all_days(self):
        return [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]

    def get_day(self, x):
        return {
            0: self.monday,
            1: self.tuesday,
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
            self.tuesday = val
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
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_groups = models.ManyToManyField(Group, verbose_name=_('User groups'))
    user_shift = models.ForeignKey(Week_shift, null=True, verbose_name=_('Week shift'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name=_('Gender'))
    date_of_employment = models.DateField(null=True, blank=True, verbose_name=_('Date of employment'))
    default_wage = models.DecimalField(
        decimal_places=2, max_digits=5, default=0, blank=True, verbose_name=_('Default wage'))

    def __init__(self, *args, **kwargs):
        super(User_profile, self).__init__(*args, **kwargs)
        if hasattr(self, 'user_shift'):
            self.old_shift = self.user_shift

    def generate_schedule(self):
        today = datetime.datetime.today()
        numdays = 60
        for x in range(0, numdays):
            date = today + datetime.timedelta(days=x)
            try:
                Schedule.objects.get(date=date, user=self, schedule=None)
            except:
                Schedule.objects.create(date=date, user=self, schedule=None)

    def get_current_working_hours(self):
        month_current = datetime.date.today()
        month_1st = month_current.replace(day=1)
        all_schedules = Schedule.objects.filter(
            date__range=[month_1st, month_current], user=self)
        time_sum = 0
        for schedule in all_schedules.all():
            # If schedule is not None
            if schedule.time_until and schedule.time_from:
                time_sum += schedule.time_until.hour - schedule.time_from.hour
        return time_sum

    def calculate_current_paycheck(self):
        return self.get_current_working_hours() * self.default_wage

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=Group)
def update_supervisor(sender, instance, created, **kwargs):
    # if instance is created and supervisor is changed
    if instance:
        try:
            new_supervisor = User_profile.objects.get(user=instance.supervisor)
        except:
            return
        new_supervisor.user_groups.add(instance)
        new_supervisor.save()

        # If first created old supervisor will be same as new
        if instance.supervisor != instance.old_supervisor:
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


@receiver(post_save, sender=User_profile)
def generate_user_schedule(sender, instance, created, *args, **kwargs):
    # If User_profile is not created then then dont generate schedule
    # If user_shift is not changed then dont generate schedule
    # If user shift is set to None then dont generate schedule
    if not created and (instance.user_shift != instance.old_shift) and instance.user_shift != None:
        month_current = datetime.date.today()
        schedules_to_remove = Schedule.objects.filter(
            Q(date__gte=month_current), user=instance)
        for schedule in schedules_to_remove:
            schedule.delete()
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

    def save(self, make_instance=False, is_swap=False, *args, **kwargs):
        # is_swap determines if save is called on swap (this lets us swap free
        # days of users)
        if (self.time_from == None or self.time_until == None) and self.user.user_shift != None and not is_swap:
            temp_shift = self.user.user_shift.get_day(self.date.weekday())

            self.time_from = temp_shift.time_from
            self.time_until = temp_shift.time_until

        if make_instance == True:
            # In case of change - followup
            try:
                old_schedule = Schedule.objects.get(pk=self.pk)
                new_followup = self
                new_followup.pk = None
                new_followup.save(is_swap=is_swap)
                old_schedule.schedule = new_followup
                old_schedule.save(is_swap=is_swap)
            except:
                pass
        # Call the "real" save() method.
        super(Schedule, self).save(*args, **kwargs)

    def is_past(self):
        return datetime.datetime.today().date() >= self.date

    def get_time_shift(self):
        if self.time_until:
            return self.time_from.strftime('%H:%M') + " - " + self.time_until.strftime('%H:%M')
        else:
            return None

    def get_string_from(self):
        if self.time_from:
            return self.date.strftime('%Y-%m-%d') + 'T' + self.time_from.strftime('%H:%M:%S')
        else:
            return None

    def get_string_until(self):
        if self.time_until:
            return self.date.strftime('%Y-%m-%d') + 'T' + self.time_until.strftime('%H:%M:%S')
        else:
            return None

    def __unicode__(self):
        return 'Schedule ' + self.date.strftime('%m/%d/%Y') + ' ' + self.user.user.first_name + ' ' + self.user.user.last_name + ' ' + str(self.pk)


class Swap(models.Model):
    schedule_1 = models.ForeignKey(Schedule, related_name='+')
    schedule_2 = models.ForeignKey(Schedule, related_name='+')
    user = models.ForeignKey(User)
    # One user can have more groups so we must define group which swap applies to
    group = models.ForeignKey(Group)
    date = models.DateField()
    permanent = models.BooleanField(default=False)
    # status determines if swap is approved by supervisor
    status = models.BooleanField(default=False)
    # if this field is true, supervisor made some action (approve/disapprove)
    resolved = models.BooleanField(default=False)

    def revert(self):
        self.save(make_instance=False)
        self.delete()

    def save(self, make_instance=True, *args, **kwargs):
        # Swap schedules(class) which enables change to be
        # visible in real schedule
        sch_1 = Schedule.objects.get(pk=self.schedule_1.pk)
        sch_2 = Schedule.objects.get(pk=self.schedule_2.pk)
        if self.status == True and make_instance == True:

            if self.permanent == True:
                today = datetime.datetime.today().date()

                filter_date_1 = (sch_1.date.weekday() % 6) + 1
                filter_date_2 = (sch_1.date.weekday() % 6) + 1

                # Filter all schedules so change is visible in the future
                all_sch_1 = Schedule.objects.filter(
                    date__week_day=filter_date_1, date__gte=today, user=sch_1.user, schedule=None).order_by('date')
                all_sch_1 = all_sch_1.exclude(pk=all_sch_1.first().pk)

                all_sch_2 = Schedule.objects.filter(
                    date__week_day=filter_date_2, date__gte=today, user=sch_2.user, schedule=None).order_by('date')
                all_sch_2 = all_sch_2.exclude(pk=all_sch_2.first().pk)

                # Change default Week_shift
                shift_1 = sch_1.user.user_shift
                shift_2 = sch_2.user.user_shift

                day_1 = shift_1.get_day(sch_1.date.weekday())
                day_2 = shift_2.get_day(sch_2.date.weekday())

                shift_1.change_day(sch_1.date.weekday(), day_2)
                shift_1.save()
                shift_2.change_day(sch_2.date.weekday(), day_1)
                shift_2.save()

                # Update future schedules
                for sc_1, sc_2 in zip(all_sch_1, all_sch_2):
                    sc_1.time_from = None
                    sc_1.time_until = None
                    sc_1.save()
                    sc_2.time_from = None
                    sc_2.time_until = None
                    sc_2.save()

            sch_1.user, sch_2.user = sch_2.user, sch_1.user
            sch_1.save(make_instance=make_instance, is_swap=True)
            sch_2.save(make_instance=make_instance, is_swap=True)

            # if days are different
            if sch_1.date != sch_2.date:
                # above were swapped free days
                # here we are swaping working shifts of two users
                # that way schedule keeps its balance
                working_shift_1 = Schedule.objects.filter(
                    user=sch_1.user, date=sch_1.date, schedule=None).exclude(time_from=None)[0]

                working_shift_2 = Schedule.objects.filter(
                    user=sch_2.user, date=sch_2.date, schedule=None).exclude(time_from=None)[0]

                working_shift_1.user, working_shift_2.user = working_shift_2.user, working_shift_1.user
                working_shift_1.save(make_instance=make_instance, is_swap=True)
                working_shift_2.save(make_instance=make_instance, is_swap=True)

        # save current state if reverse is used
        if make_instance == False:
            follow_up_1 = sch_1.schedule
            sch_1.schedule = None
            sch_1.save()
            follow_up_1.delete()

            follow_up_2 = sch_2.schedule
            sch_2.schedule = None
            sch_2.save()
            follow_up_2.delete()

        super(Swap, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Swap ' + self.date.strftime('%m/%d/%Y') + ' ' + str(self.id)
