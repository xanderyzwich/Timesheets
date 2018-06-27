from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Task, Employee, App, Defect, Adhoc, TimesheetForm


def index(request):
    # return HttpResponse("Hello, world. You're at the timesheet index.")
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'timesheets/index.html', {'form': TimesheetForm()})
    else:
        return render(request, 'timesheets/index.html', {'form': TimesheetForm()})


def apps(request):
    app_list = App.objects.all()
    template = loader.get_template('timesheets/apps.html')
    context = {
        'app_list': app_list,
    }
    return HttpResponse(template.render(context, request))


def app(request, app_id):
    app = get_object_or_404(App,pk=app_id)
    return render(request, 'timesheets/app.html', {'app': app})


