from schedule.models import Schedule
from django.core.urlresolvers import reverse

def make_events(users):
    event_list = []
    for user in users:
        schedules = Schedule.objects.filter(user=user)
        for schedule in schedules:
            event_list.append({
                "id": schedule.id,
                "title": user.user.first_name + ' ' + user.user.last_name,
                "time_from": schedule.get_string_from(),
                "time_until": schedule.get_string_until(),
                "profile_url": reverse('employee_view', kwargs={ 'employee_id': user.id }),
            })
    return event_list