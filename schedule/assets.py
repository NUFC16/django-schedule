from django_assets import Bundle, register
from django.conf import settings

schedule_less_css = Bundle(
    'schedule/static/schedule/less/schedule.less',
    depends='schedule/less/*.less',
    filters='less',
    output='schedule/gen/style_schedule.%(version)s.css',
)

schedule_css = Bundle(
    'schedule/static/schedule/css/bootstrap.min.css',
    #'schedule/static/schedule/css/calendar.min.css',
    # schedule_less_css,
    filters='cssmin',
    output='schedule/gen/schedule.%(version)s.css'
)

register('schedule_css', schedule_css)

uncompressed_js = [
    # 'schedule/lib/dataTables/datatables.js',
    # 'schedule/js/schedule.js',
]

schedule_js = Bundle(
    'schedule/static/schedule/lib/jquery/jquery-2.2.0.js',
    'schedule/static/schedule/js/bootstrap.js',
    *uncompressed_js,
    filters='jsmin',
    output='schedule/gen/no-out.min.js'
)

# this is the solution to avoid minifying already minified 3rd party lib
schedule_js_minify = Bundle(
    *uncompressed_js,
    filters='jsmin'
)

schedule_js_min = Bundle(
    'schedule/static/schedule/lib/jquery/jquery-2.2.0.min.js',
    'schedule/static/schedule/js/bootstrap.min.js',
    schedule_js_minify,
    output='schedule/gen/schedule.min.%(version)s.js'
)

if settings.DEBUG:
    register('schedule_js', schedule_js)
else:
    register('schedule_js', schedule_js_min)
