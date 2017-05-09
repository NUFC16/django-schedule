from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.core.urlresolvers import resolve


def admin(request):
    return render_to_response(
        "schedule/admin.html", {}, RequestContext(request),
    )


def employee(request):
    return render_to_response(
        "schedule/employee.html", {}, RequestContext(request),
    )


def index(request):
    return render_to_response(
        "schedule/index.html", {}, RequestContext(request),
    )
