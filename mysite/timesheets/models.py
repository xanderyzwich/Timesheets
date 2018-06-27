from django.db import models
from django.forms import ModelForm
import datetime


# Create your models here.
class Task(models.Model):
    type = models.CharField(max_length=25)    # PK

    def __str__(self):
        return self.type


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)  # PK
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.first_name) + ' ' + str(self.last_name)


class App(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name)


class Defect(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    description = models.CharField(max_length=50)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.app) + ' ' + str(self.description)


class Adhoc(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    hours_projected = models.IntegerField(default=0)
    hours_actual = models.IntegerField()
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.hours_projected) + ' ' + str(self.hours_actual) + ' ' + str(self.description)


class Timesheet(models.Model):     # PK=EMP_ID,APP_ID,TASK_TYPE,DEFECT_ID,ADHOC_ID,TASK_DATE
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    defect = models.ForeignKey(Defect, on_delete=models.PROTECT, default=None, blank=True, null=True)
    adhoc = models.ForeignKey(Adhoc, on_delete=models.PROTECT,default=None, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    hours = models.DecimalField(decimal_places=2,max_digits=4)

    def __str__(self):
        return str('Employee: ' + str(self.emp) + ' App: ' + str(self.app) + ' Task: ' + str(self.task) + ' Defect: '
                   + str(self.defect) + ' Adhoc: ' + str(self.adhoc))


class TimesheetForm(ModelForm):
    class Meta:
        model = Timesheet
        fields = ['emp', 'app', 'task', 'defect', 'adhoc', 'date', 'hours']
