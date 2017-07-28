from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    'schedule.views',
    url(r'^$', index, name='index'),
    url(r'^(?P<employee_id>\d+)/info/$', employee_view, name='employee_view'),
    url(r'^add_user/$', add_user, name='add_user_view'),
    url(r'^overview/$', groups_and_people, name='groups_and_people_view'),
)
