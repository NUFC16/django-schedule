from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import User_profile, Group
from django.contrib.auth.models import User
from schedule.forms import UserForm, UserProfileForm, EditUserForm, GroupForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.translation import ugettext as _
from schedule.utils import *


@login_required
def index(request):
    groups = User_profile.objects.get(user=request.user).user_groups
    users = User_profile.objects.filter(user_groups__in=groups.all())
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
    # Dont allow ordinary user to create users
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    if request.method == 'POST':
        user_form = UserForm(
            request.POST, is_superuser=request.user.is_superuser)
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
            up.user_groups = profile_data['user_groups']
            up.user_shift = profile_data['user_shift']
            up.save()
            messages.success(request, _(
                'Your profile was successfully created!'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm()
    return render(request, "schedule/add_user.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


@login_required
def edit_user(request, employee_id):
    # Dont allow ordinary user to create users
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    employee = User_profile.objects.get(pk=employee_id)

    data_user_profile = {
        'user_groups': employee.user_groups.all(),
        'user_shift': employee.user_shift,
    }

    if request.method == 'POST':
        user_form = EditUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data

            employee.user.first_name = user_data['first_name']
            employee.user.last_name = user_data['last_name']
            employee.user.save()

            employee.user_groups = profile_data['user_groups']
            employee.user_shift = profile_data['user_shift']
            employee.save()

            messages.success(request, _(
                'Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('groups_and_people_view'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = EditUserForm(instance=employee.user)
        profile_form = UserProfileForm(initial=data_user_profile)
    return render(request, "schedule/add_user.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def groups_and_people(request):
    # Dont allow ordinary user to manage groups and people (may be removed in
    # future)
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    # get all groups user is in
    groups = User_profile.objects.get(user=request.user).user_groups
    # get all people user is superior and dont show logged user
    employees = User_profile.objects.filter(
        user_groups__in=groups.all()).distinct().exclude(user=request.user)

    return render(request, "schedule/overview.html", {
        "groups": groups,
        "employees": employees,
    })


@login_required
def add_and_edit_group(request, group_id=None):
    # Dont allow ordinary user to manage groups and people
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    data = None
    if group_id != None:
        group = Group.objects.get(pk=group_id)
        data = {
            'group_name': group.group_name,
            'supervisor': group.supervisor
        }

    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Add group
            if group_id == None:
                Group.objects.create(
                    group_name=data['group_name'],
                    supervisor=data['supervisor']
                )
                messages.success(request, _('Group was successfully added!'))
                return HttpResponseRedirect(reverse('groups_and_people_view'))
            # edit group
            else:
                group.group_name = data['group_name']
                group.supervisor = data['supervisor']
                group.save()
                messages.success(request, _('Group was successfully edited!'))
                return HttpResponseRedirect(reverse('groups_and_people_view'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = GroupForm(initial=data)

    return render(request, "schedule/add_group.html", {
        "form": form,
    })


@login_required
def delete_group(request, group_id):
    # Dont allow ordinary user to manage groups and people
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    try:
        Group.objects.get(pk=group_id).delete()
        messages.success(request, _('Group was successfully deleted!'))
    except:
        messages.error(request, _('Group was not deleted'))

    return HttpResponseRedirect(reverse('groups_and_people_view'))
