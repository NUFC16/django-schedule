from schedule.models import Schedule, Week_shift, Swap, User_profile
from django.core.urlresolvers import reverse
import datetime


def make_events(users, logged_user, free_day_render=False):
    event_list = []
    color = ""
    for user in users:
        schedules = Schedule.objects.filter(user=user, schedule=None)
        if user == logged_user.user_profile:
            color = '#32CD32'  # lightgreen
        for schedule in schedules:
            if schedule.get_string_from() and schedule.get_string_until():
                event_list.append({
                    "id": schedule.id,
                    "title": user.user.first_name + ' ' + user.user.last_name,
                    "time_from": schedule.get_string_from(),
                    "time_until": schedule.get_string_until(),
                    "profile_url": reverse(
                        'employee_view',
                        kwargs={'employee_id': user.id}
                    ),
                    "color": color,
                })
            elif free_day_render:
                event_list.append({
                    "id": schedule.id,
                    "title": user.user.first_name + ' ' + user.user.last_name,
                    "time_from": schedule.date.strftime('%Y-%m-%d'),
                    "time_until": None,
                    "profile_url": reverse(
                        'employee_view',
                        kwargs={'employee_id': user.id}
                    ),
                    "color": color,
                })
        color = ""
    return event_list


def make_empty_events(shift):
    event_list = []
    week_day = 1
    for day in shift.get_all_days():
        if day.time_from and day.time_until:
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


def get_pending_swaps(user):
    query_1 = Swap.objects.filter(resolved=False, schedule_1__user=user)
    query_2 = Swap.objects.filter(resolved=False, schedule_2__user=user)
    return query_1 | query_2


def update_default_shift(shift):
    people = User_profile.objects.filter(user_shift=shift).distinct()
    for man in people:
        man.regenerate_schedule()
