"""Dynamic URL's to for data access"""

from django.urls import path

from . import views

app_name = 'timesheets'
urlpatterns = [
    # index page
    # time entered here
    path('', views.index, name='index'),

    # report pages
    path('report/', views.report, name='report'),
    path('report/<int:year>/', views.report, name='report'),
    path('report/<int:year>/<int:month>/', views.report, name='report'),
    path('report/<int:year>/<int:month>/<int:day>/', views.report, name='report'),

    # Adhoc Model Pages
    path('adhocs/', views.adhocs, name='adhocs'),  # list of adhocs
    path('adhoc/<int:adhoc_id>/', views.adhoc, name='adhoc'),
    path('adhoc/<int:adhoc_id>/<int:year>/', views.adhoc, name='adhoc'),
    path('adhoc/<int:adhoc_id>/<int:year>/<int:month>/', views.adhoc, name='adhoc'),
    path('adhoc/<int:adhoc_id>/<int:year>/<int:month>/<int:day>/', views.adhoc, name='adhoc'),

    # App Model Pages
    path('apps/', views.apps, name='apps'),     # list of applications supported
    path('app/', views.apps, name='apps'),      # alternate url in case app id is removed from specific page
    path('app/<int:app_id>/', views.app, name='app'),
    path('app/<int:app_id>/<int:year>/', views.app, name='app'),
    path('app/<int:app_id>/<int:year>/<int:month>/', views.app, name='app'),
    path('app/<int:app_id>/<int:year>/<int:month>/<int:day>/', views.app, name='app'),

    # Defect Model Pages
    path('defects/', views.defects, name='defects'),  # list of defects
    path('defect/', views.defects, name='defects'),  # alternate url in case defect id is removed from specific page
    path('defect/<int:defect_id>/', views.defect, name='defect'),
    path('defect/<int:defect_id>/<int:year>/', views.defect, name='defect'),
    path('defect/<int:defect_id>/<int:year>/<int:month>/', views.defect, name='defect'),
    path('defect/<int:defect_id>/<int:year>/<int:month>/<int:day>/', views.defect, name='defect'),

    # Employee Model Pages
    path('employees/', views.employees, name='employees'),      # list of employees
    path('employee/', views.employees, name='employees'),       # alternate url in case employee id is removed from specific page
    path('employee/<int:employee_id>/', views.employee, name='employee'),
    path('employee/<int:employee_id>/<int:year>/', views.employee, name='employee'),
    path('employee/<int:employee_id>/<int:year>/<int:month>/', views.employee, name='employee'),
    path('employee/<int:employee_id>/<int:year>/<int:month>/<int:day>/', views.employee, name='employee'),

    # Task Model Pages
    path('tasks/', views.tasks, name='tasks'),  # list of tasks
    path('task/', views.tasks, name='tasks'),   # alternate url in case task id is removed from specific page
    path('task/<int:task_id>/', views.task, name='task'),
    path('task/<int:task_id>/<int:year>/', views.task, name='task'),
    path('task/<int:task_id>/<int:year>/<int:month>/', views.task, name='task'),
    path('task/<int:task_id>/<int:year>/<int:month>/<int:day>/', views.task, name='task'),

]