from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    'schedule.views',
    url(r'^$', index, name='index'),
    url(r'^(?P<employee_id>\d+)/info/$', employee_view, name='employee_view'),
    url(r'^add_user/$', add_user, name='add_user_view'),
    url(r'^(?P<employee_id>\d+)/edit_user/$', edit_user, name='edit_user_view'),
    url(r'^overview/$', groups_and_people, name='groups_and_people_view'),
    url(r'^add_group/$', add_and_edit_group, name='add_group_view'),
    url(r'^(?P<group_id>\d+)/edit_group/$', add_and_edit_group, name='edit_group_view'),
    url(r'^(?P<group_id>\d+)/delete_group/$', delete_group, name='delete_group_view'),
    url(r'^(?P<shift_id>\d+)/shift/$', shift_view, name='shift_view'),
    url(r'^(?P<shift_id>\d+)/delete_shift/$', delete_shift, name='delete_shift_view'),
    url(r'^add_shift/$', add_shift, name='add_shift_view'),
)
