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


def report(request, year=0, month=0, day=0):
    """Used to generate report of all labor in a given year, month or day"""

    limited = time_limit(Timesheet.objects.all(), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': 'Timesheet', 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Views tied to models
# Listed alphabetically

# Adhoc Model Views
def adhocs(request):
    """List of all adhoc task entries"""

    adhoc_list = Adhoc.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': adhoc_list,
        'title': 'Adhoc Tasks',
        'object_model': 'adhoc',
    }
    return HttpResponse(template.render(context, request))


def adhoc(request, adhoc_id, year=0, month=0, day=0):
    """Summary and data for a specific adhoc entry"""

    adhoc = get_object_or_404(Adhoc, pk=adhoc_id)
    limited = time_limit(Timesheet.objects.filter(adhoc__id=adhoc_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': adhoc, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# App Model Views
def apps(request):
    """List of all app entries"""

    app_list = App.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': app_list,
        'title': 'Supported Apps',
        'object_model': 'app',
    }
    return HttpResponse(template.render(context, request))


def app(request, app_id, year=0, month=0, day=0):
    """Summary and data for a specific app"""

    app = get_object_or_404(App,pk=app_id)
    limited = time_limit(Timesheet.objects.filter(app__id=app_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': app, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Defect Model Views
def defects(request):
    """List of all defect entries"""

    defect_list = Defect.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': defect_list,
        'title': 'Supported Defects',
        'object_model': 'defect',
    }
    return HttpResponse(template.render(context, request))


def defect(request, defect_id, year=0, month=0, day=0):
    """Summary and data for a specific defect"""

    defect = get_object_or_404(Defect, pk=defect_id)
    limited = time_limit(Timesheet.objects.filter(defect__id=defect_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': defect, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Employee Model Views
def employees(request):
    """List of all support employees"""

    employee_list = Employee.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': employee_list,
        'title': 'Support Employees',
        'object_model': 'employee',
    }
    return HttpResponse(template.render(context, request))


def employee(request, employee_id, year=0, month=0, day=0):
    """Summary and data for a specific employee"""

    employee = get_object_or_404(Employee, pk=employee_id)
    limited = time_limit(Timesheet.objects.filter(emp__id=employee_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': employee, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Task Model Views
def tasks(request):
    """List of all tasks (includes adhoc and defect collective data)"""

    task_list = Task.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': task_list,
        'title': 'Support Tasks',
        'object_model': 'task',
    }
    return HttpResponse(template.render(context, request))


def task(request, task_id, year=0, month=0, day=0):
    """Summary and data for a specific task (or the adhoc/defect collection)"""

    task = get_object_or_404(Task, pk=task_id)
    limited = time_limit(Timesheet.objects.filter(task__id=task_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': task, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Summarize the result_set by employee
def summary(result_set):
    """Generate summary by employee from full data list"""

    return result_set.values('emp__id', 'emp__first_name', 'emp__last_name').order_by().annotate(sum=Sum('hours'))


# filter the result_set by year, month, and day as requested
def time_limit(result_set, year, month, day):
    """Limit result_set to a given time period"""

    today = datetime.date.today()
    time_string = ' report for '
    if day == 0:
        if month == 0:
            if year == 0:
                timesheet_list = result_set.filter(date__month=today.month, date__year=today.year)
                time_string += "this month"
            else:
                timesheet_list = result_set.filter(date__year=year)
                time_string += str(year)
        else:
            timesheet_list = result_set.filter(date__month=month, date__year=year)
            time_string += calendar.month_name[month] + ' ' + str(year)

    else:
        timesheet_list = result_set.filter(date__month=month, date__year=year, date__day=day)
        time_string += str(day) + ' ' + calendar.month_name[month] + ' ' + str(year)
    return timesheet_list, time_string
