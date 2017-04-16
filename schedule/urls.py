from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    'schedule.views',
    url(r'^admin/$', admin, name='schedule_admin'),
    url(r'^employee/$', employee, name='schedule_employee'),
)
