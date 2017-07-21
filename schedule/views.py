from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import Schedule, User, Group
import datetime
import pdb

group = Group.objects.first()


def make_events(users):
    event_list = []
    for user in users:
        schedules = Schedule.objects.filter(user=user)
        for schedule in schedules:
            event_list.append({"id": schedule.id,
                               "title": user.first_name + ' ' + user.last_name,
                               "time_from": schedule.get_string_from(),
                               "time_until": schedule.get_string_until()
                               })
    return event_list


def index(request):
    users = User.objects.filter(user_group=group)
    # generira se raspored unaprijed ako nije vec postojeci
    for user in users:
        user.generate_schedule()
    events = make_events(users)
    return render(request, "schedule/index.html", {
        "users": users,
        "events": events,
    })
