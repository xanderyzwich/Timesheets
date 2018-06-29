import calendar
import datetime

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
    else:
        return render(request, 'timesheets/index.html', {'form': TimesheetForm()})


def report(request, year=0, month=0, day=0):
    today = datetime.date.today()
    if day == 0:
        if month == 0:
            if year == 0:
                timesheet_list = Timesheet.objects.filter(date__month=today.month, date__year=today.year)
                time_string = "this month"
            else:
                timesheet_list = Timesheet.objects.filter(date__year=year)
                time_string = str(year)
        else:
            timesheet_list = Timesheet.objects.filter(date__month=month, date__year=year)
            time_string = calendar.month_name[month] + ' ' + str(year)

    else:
        timesheet_list = Timesheet.objects.filter(date__month=month, date__year=year, date__day=day)
        time_string = str(day) + ' ' + calendar.month_name[month] + ' ' + str(year)

    return render(request, 'timesheets/timesheet.html', {'object': 'Timesheet report for ' + time_string,
                                                          'timesheet_list': timesheet_list})


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


def adhoc(request, adhoc_id):
    adhoc = get_object_or_404(Adhoc, pk=adhoc_id)
    today_date = datetime.date.today()
    timesheet_list = Timesheet.objects.filter(date__month=today_date.month,date__year=today_date.year,
                                              adhoc__id=adhoc_id)
    return render(request, 'timesheets/timesheet.html', {'object': adhoc, 'timesheet_list': timesheet_list})


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


def app(request, app_id):
    app = get_object_or_404(App,pk=app_id)
    today_date = datetime.date.today()
    timesheet_list = Timesheet.objects.filter(date__month=today_date.month, date__year=today_date.year, app__id=app_id)
    return render(request, 'timesheets/timesheet.html', {'object': app, 'timesheet_list': timesheet_list})


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


def defect(request, defect_id):
    defect = get_object_or_404(Defect, pk=defect_id)
    today_date = datetime.date.today()
    timesheet_list = Timesheet.objects.filter(date__month=today_date.month, date__year=today_date.year,
                                              defect__id=defect_id)
    return render(request, 'timesheets/timesheet.html', {'object': defect, 'timesheet_list': timesheet_list})


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


def employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    today_date = datetime.date.today()
    timesheet_list = Timesheet.objects.filter(date__month=today_date.month, date__year=today_date.year, emp__id=employee_id)
    return render(request, 'timesheets/timesheet.html', {'object': employee, 'timesheet_list': timesheet_list})


# Task Model Views
def tasks(request):
    task_list = Task.objects.all()
    template = loader.get_template('timesheets/list.html')
    context = {
        'object_list': task_list,
        'title': 'Support Tasks',
        'object_url': 'task',
    }
    return HttpResponse(template.render(context, request))


def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    today_date = datetime.date.today()
    timesheet_list = Timesheet.objects.filter(date__month=today_date.month, date__year=today_date.year, task__id=task_id)
    return render(request, 'timesheets/timesheet.html', {'object': task, 'timesheet_list': timesheet_list})
