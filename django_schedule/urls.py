from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    url(r'^login/$', auth_views.login, name='login'),
    url(
        r'^logout/$', auth_views.logout,
        {'next_page': '/login'}, name='logout'
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schedule/', include('schedule.urls')),
)
