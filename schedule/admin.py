from django.contrib import admin
from schedule.models import *


all_models = [Staff, User, Group, Day_shift,
              Week_shift, Swap, Schedule, Permanent_swap]

admin.site.register(all_models)
