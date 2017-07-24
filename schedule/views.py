from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import User_profile, Group
from django.contrib.auth.decorators import login_required

from schedule.utils import *

@login_required
def index(request):
    group = User_profile.objects.get(user=request.user).user_group
    users = User_profile.objects.filter(user_group=group)
    # generate schedule in advance if it does not exist
    for user in users:
        user.generate_schedule()
    events = make_events(users)
    return render(request, "schedule/index.html", {
        "users": users,
        "events": events,
    })
