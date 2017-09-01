from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template.context import RequestContext
from django.core.urlresolvers import resolve

from schedule.models import User_profile, Group, Week_shift, Day_shift, Swap
from django.contrib.auth.models import User
from schedule.forms import UserForm, UserProfileForm, EditUserForm, GroupForm, ShiftForm, SwapForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.translation import ugettext as _
from schedule.utils import *


@login_required
def index(request):
    groups = User_profile.objects.get(user=request.user).user_groups
    # user can be in more groups so distinct is needed
    users = User_profile.objects.filter(
        user_groups__in=groups.all()).distinct()
    # generate schedule in advance if it does not exist
    for user in users:
        user.generate_schedule()
    events = make_events(users, request.user)
    return render(request, "schedule/index.html", {
        "user": request.user.user_profile,
        "users": users,
        "events": events,
    })


@login_required
def employee_info(request, employee_id):
    user = User_profile.objects.get(pk=employee_id)
    return render(request, "schedule/employee_info.html", {
        "user": user,
    })


@login_required
def delete_user(request, employee_id):
    # Only superuser can delete employees
    if not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    try:
        employee = User_profile.objects.get(pk=employee_id)
        employee.user.delete()
        employee.delete()
        messages.success(request, _('User was successfully deleted!'))
    except:
        messages.error(request, _('User was not deleted'))

    return HttpResponseRedirect(reverse('groups_and_people_view'))


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
                password=user_data['password1']
            )
            u.is_staff = user_data['is_staff']
            u.is_superuser = user_data['is_superuser']
            u.save()

            up = User_profile.objects.get(user=u)

            field_attributes = [
                "user_groups", "user_shift", "date_of_birth",
                "date_of_employment", "gender", "default_wage"
            ]

            for field in field_attributes:
                setattr(up, field, profile_data[field])
            up.save()

            messages.success(request, _(
                'Your profile was successfully created!'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm()

    # logged user (must be supervisor) can only assign groups for which he has rights
    groups = request.user.user_profile.user_groups.all()
    profile_form.fields["user_groups"].queryset = groups
    profile_form.fields["user_shift"].queryset = Week_shift.objects.filter(week_group__in=groups)
    return render(request, "schedule/add_user.html", {
        "user": request.user.user_profile,
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
        'date_of_birth': employee.date_of_birth,
        'date_of_employment': employee.date_of_employment,
        'gender': employee.gender,
        'default_wage': employee.default_wage,
    }

    if request.method == 'POST':
        user_form = EditUserForm(
            request.POST, is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data

            employee.user.first_name = user_data['first_name']
            employee.user.last_name = user_data['last_name']
            employee.user.save()

            field_attributes = [
                "user_groups", "user_shift", "date_of_birth",
                "date_of_employment", "gender", "default_wage"
            ]

            for field in field_attributes:
                setattr(employee, field, profile_data[field])
            employee.save()

            messages.success(request, _(
                'Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('groups_and_people_view'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = EditUserForm(
            instance=employee.user, is_superuser=request.user.is_superuser)
        profile_form = UserProfileForm(initial=data_user_profile)
    return render(request, "schedule/add_user.html", {
        "user": request.user.user_profile,
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
        user_groups__in=groups.all(), user__is_superuser=False).distinct().exclude(user=request.user)

    return render(request, "schedule/overview.html", {
        "user": request.user.user_profile,
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

    form.fields["supervisor"].label_from_instance = lambda obj: "%s" % (
        obj.first_name + " " + obj.last_name)
    return render(request, "schedule/add_group.html", {
        "user": request.user.user_profile,
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


@login_required
def shift_view(request, shift_id):
    # Dont allow ordinary user to edit shifts
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    shift = Week_shift.objects.get(pk=shift_id)

    if request.method == 'POST':
        form_labels = [
            ("monday", "day1_from", "day1_until"),
            ("tuesday", "day2_from", "day2_until"),
            ("wednesday", "day3_from", "day3_until"),
            ("thursday", "day4_from", "day4_until"),
            ("friday", "day5_from", "day5_until"),
            ("saturday", "day6_from", "day6_until"),
            ("sunday", "day0_from", "day0_until")
        ]

        for day, post_time_from, post_time_until in form_labels:
            current_from = request.POST.get(post_time_from)
            current_until = request.POST.get(post_time_until)

            if current_from != None and current_until != None:
                current_from = datetime.datetime.strptime(
                    current_from, '%H:%M:%S').time()
                current_until = datetime.datetime.strptime(
                    current_until, '%H:%M:%S').time()

            try:
                day_object = getattr(shift, day)
                setattr(day_object, 'time_from', current_from)
                setattr(day_object, 'time_until', current_until)
                day_object.save()
                shift.save()
            except:
                messages.error(request, _('Shift was not updated!'))
                break
            if day == form_labels[-1][0]:
                messages.success(request, _('Shift was successfully updated!'))

    events = make_empty_events(shift)
    return render(request, "schedule/shift_view.html", {
        "user": request.user.user_profile,
        "events": events,
        "shift": shift,
    })


@login_required
def delete_shift(request, shift_id):
    # Dont allow ordinary user to delete shifts
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    shift = Week_shift.objects.get(pk=shift_id)
    # This is used in order to secure integrity of the base
    user_profiles = User_profile.objects.filter(user_shift=shift)
    for user in user_profiles:
        user.user_shift = None
        user.save()
    try:
        shift.delete()
        messages.success(request, _('Shift was successfully deleted!'))
    except:
        messages.error(request, _('Shift was not deleted'))

    return HttpResponseRedirect(reverse('groups_and_people_view'))


@login_required
def add_shift(request, group_id):
    # Dont allow ordinary user to add shifts for certain group
    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    group = Group.objects.get(pk=group_id)

    if request.method == 'POST':
        form = ShiftForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            day_shifts = {}
            form_labels = [
                ("monday", "day1_from", "day1_until"),
                ("tuesday", "day2_from", "day2_until"),
                ("wednesday", "day3_from", "day3_until"),
                ("thursday", "day4_from", "day4_until"),
                ("friday", "day5_from", "day5_until"),
                ("saturday", "day6_from", "day6_until"),
                ("sunday", "day0_from", "day0_until")
            ]

            for day, time_from, time_until in form_labels:
                day_shifts[day] = Day_shift.objects.create(
                    time_from=request.POST.get(time_from),
                    time_until=request.POST.get(time_until)
                )

            Week_shift.objects.create(
                name=data["name"],
                monday=day_shifts["monday"],
                tuesday=day_shifts["tuesday"],
                wednesday=day_shifts["wednesday"],
                thursday=day_shifts["thursday"],
                friday=day_shifts["friday"],
                saturday=day_shifts["saturday"],
                sunday=day_shifts["sunday"],
                week_group=group
            )
            messages.success(request, _('Shift was successfully added!'))
            return HttpResponseRedirect(reverse('groups_and_people_view'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = ShiftForm(initial={"week_group": group})

    return render(request, "schedule/add_shift.html", {
        "user": request.user.user_profile,
        "form": form,
    })

@login_required
def confirm_receiver_swap(request, group_id, swap_id):

    swap = Swap.objects.get(pk=swap_id)

    if swap.schedule_1.user != request.user.user_profile:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    try:
        swap.receiver_status = True
        swap.save()
        messages.success(request, _('Swap was successfully confirmed!'))
    except:
        messages.error(request, _('Swap was not confirmed!'))

    return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))

def reject_receiver_swap(request, group_id, swap_id):

    swap = Swap.objects.get(pk=swap_id)

    if swap.schedule_1.user != request.user.user_profile:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    try:
        swap.delete()
        messages.success(request, _('Swap was successfully dropped!'))
    except:
        messages.error(request, _('Swap was not dropped!'))

    return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))

@login_required
def confirm_swap(request, group_id, swap_id):

    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    try:
        swap = Swap.objects.get(pk=swap_id)
        swap.status = True
        swap.resolved = True
        swap.save()
        messages.success(request, _('Swap was successfully confirmed!'))
    except:
        messages.error(request, _('Swap was not confirmed!'))

    return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))


@login_required
def reject_swap(request, group_id, swap_id):

    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    swap = Swap.objects.get(pk=swap_id)
    try:
        swap.status = False
        swap.resolved = True
        swap.save()
        messages.success(request, _('Swap was successfully rejected!'))
    except:
        messages.error(request, _('Swap was not rejected!'))

    return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))


@login_required
def revert_swap(request, group_id, swap_id):

    if not request.user.is_staff or not request.user.is_superuser:
        HttpResponseForbidden('<h1>Permission denied</h1>')

    swap = Swap.objects.get(pk=swap_id)
    try:
        swap.revert()
        messages.success(request, _('Swap was successfully erased!'))
    except:
        messages.error(request, _('Swap was not reverted!'))

    return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))


@login_required
def swaps(request, group_id):
    # get all groups user is in
    group = Group.objects.get(pk=group_id)

    if request.user.is_staff or request.user.is_superuser:
        pending_swaps = Swap.objects.filter(resolved=False, group=group)
        resolved_swaps = Swap.objects.filter(
            resolved=True, group=group)
    else:
        pending_swaps = get_pending_swaps(request.user.user_profile)
        resolved_swaps = Swap.objects.filter(
            resolved=True, group=group, user=request.user)

    # get all people user is superior and dont show logged user
    employees = User_profile.objects.filter(
        user_groups=group, user__is_staff=False).exclude(user=request.user)

    # True is for free day render
    events_others = make_events(employees, request.user, True)
    # If its supervisor then he can change all shift of his employees
    events_logged = events_others
    if not request.user.is_staff or not request.user.is_superuser:
        # If its employee he can only swap his shift for someone elses
        events_logged = make_events(
            [request.user.user_profile], request.user, True)

    if request.method == 'POST':
        form = SwapForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            confirmation_status = False
            resolved = False
            if request.user.is_staff or request.user.is_superuser:
                confirmation_status = True
                resolved = True
            try:
                Swap.objects.create(
                    schedule_1=data["schedule_1"],
                    schedule_2=data["schedule_2"],
                    group=group,
                    user=request.user,
                    date=datetime.datetime.today().date(),
                    permanent=data["permanent"],
                    status=confirmation_status,
                    resolved=resolved
                )
                messages.success(request, _('Swap was successfully sent!'))
            except:
                messages.error(request, _('Swap was not created!'))
            return HttpResponseRedirect(reverse('swaps_view', kwargs={"group_id": group_id}))
        else:
            messages.error(request, _('Please correct the error above.'))
    else:
        form = SwapForm()
    return render(request, "schedule/swaps.html", {
        "user": request.user.user_profile,
        "group": group,
        "pending_swaps": pending_swaps,
        "resolved_swaps": resolved_swaps,
        "events_others": events_others,
        "events_logged": events_logged,
        "form": form,
    })
