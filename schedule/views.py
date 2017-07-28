from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import User_profile, Group
from django.contrib.auth.models import User
from schedule.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.translation import ugettext as _
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


@login_required
def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data
            u = User.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password1'],
            )
            up = User_profile.objects.get(user=u)
            up.user_group = profile_data['user_group']
            up.user_shift = profile_data['user_shift']
            up.save()
            messages.success(request, _(
                'Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm()
    return render(request, 'schedule/add_user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
