from schedule.models import Schedule, Week_shift
from django.core.urlresolvers import reverse
import datetime


def make_events(users, logged_user):
    event_list = []
    color = ""
    for user in users:
        schedules = Schedule.objects.filter(user=user)
        if user == logged_user.user_profile:
            color = 'green'
        for schedule in schedules:
            if not schedule.get_string_from() == None and not schedule.get_string_until() == None:
                event_list.append({
                    "id": schedule.id,
                    "title": user.user.first_name + ' ' + user.user.last_name,
                    "time_from": schedule.get_string_from(),
                    "time_until": schedule.get_string_until(),
                    "profile_url": reverse('employee_view', kwargs={'employee_id': user.id}),
                    "color": color,
                })
        color = ""
    return event_list


def make_empty_events(shift):
    event_list = []
    week_day = 1
    for day in shift.get_all_days():
        if not day.time_from == None and not day.time_until == None:
            event_list.append({
                # id is a number 0-7 depending on a day
                "id": week_day,
                "title": "",
                "time_from": day.time_from.strftime('%H:%M:%S'),
                "time_until": day.time_until.strftime('%H:%M:%S'),
                "profile_url": "",
                "color": "",
                "repeat": week_day,
            })

        week_day = (week_day + 1) % 7
    return event_list
