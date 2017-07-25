from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import User_profile, Group
from django.contrib.auth.decorators import login_required

from schedule.utils import *

@login_required
def index(request):
    group = User_profile.objects.get(user=request.user).user_group
    users = User_profile.objects.filter(user_group__in=group.all())
    # generate schedule in advance if it does not exist
    for user in users:
        user.generate_schedule()
    events = make_events(users)
    return render(request, "schedule/index.html", {
        "users": users,
        "events": events,
    })

@login_required
def employee_view(request, employee_id):
    user = User_profile.objects.get(pk=employee_id)
    return render(request, "schedule/employee_info.html", {
        "user": user,
    })
