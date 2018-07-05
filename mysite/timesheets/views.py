"""Django views for the Timesheet application"""

import calendar
import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Task, Employee, App, Defect, Adhoc, Timesheet, TimesheetForm


# Views not tied to a model
def index(request):
    """Timesheet entry view utilizes Form defined in models.py"""

    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'timesheets/index.html', {'form': TimesheetForm()})


def report(request, year=None, month=None, day=None):
    """Used to generate report of all labor in a given year, month or day"""

    limited, time_string = time_limit(year, month, day)
    context = {
        'object': 'Timesheet',
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
    }
    return render(request, 'timesheets/timesheet.html', context)


# Views tied to models
# Listed alphabetically

# Adhoc Model Views
def adhocs(request):
    """List of all adhoc task entries"""

    adhoc_list = Adhoc.objects.all()
    data_list = list()
    for item in adhoc_list:
        hours = Timesheet.objects.filter(adhoc__id=item.id).aggregate(sum=Sum('hours')).get('sum')
        if hours is None:
            hours = 0
        if int(item.hours_projected) > 0:
            item.description += ' - ' + str(item.hours_projected) + ' hours'
        data_list.append(ListItem(item.id, item.description, hours))
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': data_list,
        'title': 'Adhoc Tasks',
        'object_model': 'adhoc'
    }
    return HttpResponse(template.render(context, request))


def adhoc(request, adhoc_id, year=None, month=None, day=None):
    """Summary and data for a specific adhoc entry"""

    adhoc = get_object_or_404(Adhoc, pk=adhoc_id)
    limited, time_string = time_limit(year, month, day)
    limited = limited.filter(adhoc__id=adhoc_id)
    context = {
        'object': adhoc,
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
    }
    return render(request, 'timesheets/timesheet.html', context)


# App Model Views
def apps(request):
    """List of all app entries"""

    app_list = App.objects.all()
    data_list = list()
    for item in app_list:
        hours = Timesheet.objects.filter(app__id=item.id).aggregate(sum=Sum('hours')).get('sum')
        if hours is None:
            hours = str(0)
        data_list.append(ListItem(item.id, str(item.name), hours))
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': data_list,
        'title': 'Supported Apps',
        'object_model': 'app',
    }
    return HttpResponse(template.render(context, request))


def app(request, app_id, year=None, month=None, day=None):
    """Summary and data for a specific app"""

    app = get_object_or_404(App,pk=app_id)
    limited, time_string = time_limit(year, month, day)
    limited = limited.filter(app__id=app_id)
    context = {
        'object': app,
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
    }
    return render(request, 'timesheets/timesheet.html', context)


# Defect Model Views
def defects(request):
    """List of all defect entries"""

    defect_list = Defect.objects.all()
    data_list = list()
    for item in defect_list:
        hours = Timesheet.objects.filter(defect__id=item.id).aggregate(sum=Sum('hours')).get('sum')
        if hours is None:
            hours = str(0)
        data_list.append(ListItem(item.id, str(item.app) + ': ' + str(item.description), hours))
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': data_list,
        'title': 'Supported Defects',
        'object_model': 'defect',
    }
    return HttpResponse(template.render(context, request))


def defect(request, defect_id, year=None, month=None, day=None):
    """Summary and data for a specific defect"""

    defect = get_object_or_404(Defect, pk=defect_id)
    limited, time_string = time_limit(year, month, day)
    limited = limited.filter(defect__id=defect_id)
    context = {
        'object': defect,
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
     }
    return render(request, 'timesheets/timesheet.html', context)


# Employee Model Views
def employees(request):
    """List of all support employees"""

    employee_list = Employee.objects.all()
    data_list = list()
    for item in employee_list:
        hours = Timesheet.objects.filter(emp__id=item.id).aggregate(sum=Sum('hours')).get('sum')
        if hours is None:
            hours = str(0)
        data_list.append(ListItem(item.id, item.name(), hours))
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': data_list,
        'title': 'Support Employees',
        'object_model': 'employee',
    }
    return HttpResponse(template.render(context, request))


def employee(request, employee_id, year=None, month=None, day=None):
    """Summary and data for a specific employee"""

    employee = get_object_or_404(Employee, pk=employee_id)
    limited, time_string = time_limit(year, month, day)
    limited = limited.filter(emp__id=employee_id)
    context = {
        'object': employee,
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
    }
    return render(request, 'timesheets/timesheet.html', context)


# Task Model Views
def tasks(request):
    """List of all tasks (includes adhoc and defect collective data)"""

    task_list = Task.objects.all()
    data_list = list()
    for item in task_list:
        hours = Timesheet.objects.filter(task__type=item.type).aggregate(sum=Sum('hours')).get('sum')
        if hours is None:
            hours = str(0)
        data_list.append(ListItem(item.id, item.type, hours))
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': data_list,
        'title': 'Support Tasks',
        'object_model': 'task',
    }
    return HttpResponse(template.render(context, request))


def task(request, task_id, year=None, month=None, day=None):
    """Summary and data for a specific task (or the adhoc/defect collection)"""

    task = get_object_or_404(Task, pk=task_id)
    limited, time_string = time_limit(year, month, day)
    limited = limited.filter(task__id=task_id)
    context = {
        'object': task,
        'report': time_string,
        'data': summary(limited),
        'timesheet_list': limited,
        'total': limited.aggregate(Sum('hours'))
    }
    return render(request, 'timesheets/timesheet.html', context)


# Summarize the result_set by employee
def summary(result_set):
    """Generate summary by employee from full data list"""

    return result_set.values('emp__id', 'emp__first_name', 'emp__last_name').order_by().annotate(sum=Sum('hours'))


# filter the result_set by year, month, and day as requested
def time_limit(year, month, day):
    """Return timesheet entries for a given time period, also a time_string for display use"""

    today = datetime.date.today()
    time_string = ' report for '
    if day is None:
        if month is None:
            if year is None:
                timesheet_list = Timesheet.objects.filter(date__month=today.month, date__year=today.year)
                time_string += "this month"
            else:
                timesheet_list = Timesheet.objects.filter(date__year=year)
                time_string += str(year)
        else:
            timesheet_list = Timesheet.objects.filter(date__month=month, date__year=year)
            time_string += calendar.month_name[month] + ' ' + str(year)

    else:
        timesheet_list = Timesheet.objects.filter(date__month=month, date__year=year, date__day=day)
        time_string += str(day) + ' ' + calendar.month_name[month] + ' ' + str(year)
    return timesheet_list, time_string

class ListItem:
    def __init__(self, id, description, total):
        self.id = id
        self.description = description
        self.total = total