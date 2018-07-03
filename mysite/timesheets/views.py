import calendar
import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Task, Employee, App, Defect, Adhoc, Timesheet, TimesheetForm


# Views not tied to a model
def index(request):
    # return HttpResponse("Hello, world. You're at the timesheet index.")
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'timesheets/index.html', {'form': TimesheetForm()})


def report(request, year=0, month=0, day=0):
    limited = time_limit(Timesheet.objects.all(), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': 'Timesheet', 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Views tied to models
# Listed alphabetically

# Adhoc Model Views
def adhocs(request):
    adhoc_list = Adhoc.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': adhoc_list,
        'title': 'Adhoc Tasks',
        'object_model': 'adhoc',
    }
    return HttpResponse(template.render(context, request))


def adhoc(request, adhoc_id, year=0, month=0, day=0):
    adhoc = get_object_or_404(Adhoc, pk=adhoc_id)
    limited = time_limit(Timesheet.objects.filter(adhoc__id=adhoc_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': adhoc, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# App Model Views
def apps(request):
    app_list = App.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': app_list,
        'title': 'Supported Apps',
        'object_model': 'app',
    }
    return HttpResponse(template.render(context, request))


def app(request, app_id, year=0, month=0, day=0):
    app = get_object_or_404(App,pk=app_id)
    limited = time_limit(Timesheet.objects.filter(app__id=app_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': app, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Defect Model Views
def defects(request):
    defect_list = Defect.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': defect_list,
        'title': 'Supported Defects',
        'object_model': 'defect',
    }
    return HttpResponse(template.render(context, request))


def defect(request, defect_id, year=0, month=0, day=0):
    defect = get_object_or_404(Defect, pk=defect_id)
    limited = time_limit(Timesheet.objects.filter(defect__id=defect_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': defect, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Employee Model Views
def employees(request):
    employee_list = Employee.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': employee_list,
        'title': 'Support Employees',
        'object_model': 'employee',
    }
    return HttpResponse(template.render(context, request))


def employee(request, employee_id, year=0, month=0, day=0):
    employee = get_object_or_404(Employee, pk=employee_id)
    limited = time_limit(Timesheet.objects.filter(emp__id=employee_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': employee, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Task Model Views
def tasks(request):
    task_list = Task.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': task_list,
        'title': 'Support Tasks',
        'object_model': 'task',
    }
    return HttpResponse(template.render(context, request))


def task(request, task_id, year=0, month=0, day=0):
    task = get_object_or_404(Task, pk=task_id)
    limited = time_limit(Timesheet.objects.filter(task__id=task_id), year, month, day)
    return render(request, 'timesheets/timesheet.html',
                  {'object': task, 'report': limited[1], 'data': summary(limited[0]), 'timesheet_list': limited[0]})


# Summarize the result_set by employee
def summary(result_set):
    return result_set.values('emp__id', 'emp__first_name', 'emp__last_name').order_by().annotate(sum=Sum('hours'))


# filter the result_set by year, month, and day as requested
def time_limit(result_set, year, month, day):
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
