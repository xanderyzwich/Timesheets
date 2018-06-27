from django.contrib import admin
from .models import Task, Employee, App, Defect, Adhoc, Timesheet


# Register your models here.
admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(App)
admin.site.register(Defect)
admin.site.register(Adhoc)
admin.site.register(Timesheet)
