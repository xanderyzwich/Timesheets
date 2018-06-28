from django.urls import path

from . import views

app_name = 'timesheets'
urlpatterns = [
    # index page
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('report/<int:year>/', views.report, name='report'),
    path('report/<int:year>/<int:month>/', views.report, name='report'),
    path('report/<int:year>/<int:month>/<int:day>/', views.report, name='report'),

    # Adhoc Model Pages
    path('adhocs/', views.adhocs, name='adhocs'),  # list of adhocs
    path('adhoc/', views.adhocs, name='adhocs'),   # alternate url in case adhoc id is removed from specific page
    path('adhoc/<int:adhoc_id>/', views.adhoc, name='adhoc'),

    # App Model Pages
    path('apps/', views.apps, name='apps'),     # list of applications supported
    path('app/', views.apps, name='apps'),      # alternate url in case app id is removed from specific page
    path('app/<int:app_id>/', views.app, name='app'),

    # Defect Model Pages
    path('defects/', views.defects, name='defects'),  # list of defects
    path('defect/', views.defects, name='defects'),  # alternate url in case defect id is removed from specific page
    path('defect/<int:defect_id>/', views.defect, name='defect'),

    # Employee Model Pages
    path('employees/', views.employees, name='employees'),      # list of employees
    path('employee/', views.employees, name='employees'),       # alternate url in case employee id is removed from specific page
    path('employee/<int:employee_id>/', views.employee, name='employee'),

    # Task Model Pages
    path('tasks/', views.tasks, name='tasks'),  # list of tasks
    path('task/', views.tasks, name='tasks'),   # alternate url in case task id is removed from specific page
    path('task/<int:task_id>/', views.task, name='task'),

]