from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    'schedule.views',
    url(r'^$', index, name='index'),
)
