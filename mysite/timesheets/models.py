"""The database models and form based on the timesheet model"""

import datetime

from django.db import models
from django.forms import ModelForm, ValidationError


# Create your models here.
class Task(models.Model):
    """Used to support Timesheet class"""

    type = models.CharField(max_length=25)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return self.type


class Employee(models.Model):
    """Used to support Timesheet class"""

    id = models.IntegerField(primary_key=True)  # PK
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    created_date = models.DateField(default=datetime.date.today)

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return str(self.id) + ' ' + str(self.first_name) + ' ' + str(self.last_name)


class App(models.Model):
    """Used to support Timesheet class"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name)


class Defect(models.Model):
    """Used to support Timesheet class"""

    id = models.CharField(primary_key=True, max_length=25)
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    description = models.CharField(max_length=50)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.id) + ' ' + str(self.app) + ' ' + str(self.description)


class Adhoc(models.Model):
    """Used to support Timesheet class"""

    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    hours_projected = models.IntegerField(default=0)
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        output = 'Adhoc Task: ' + str(self.id) + ' - ' + str(self.description)
        if int(self.hours_projected) > 0:
            output += ' (' + str(self.hours_projected) + ' hours projected)'
        return output


class Timesheet(models.Model):     # PK=EMP_ID,APP_ID,TASK_TYPE,DEFECT_ID,ADHOC_ID,TASK_DATE
    """Primary class/table for this application"""

    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    defect = models.ForeignKey(Defect, on_delete=models.PROTECT, default=None, blank=True, null=True)
    adhoc = models.ForeignKey(Adhoc, on_delete=models.PROTECT,default=None, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    hours = models.DecimalField(decimal_places=2,max_digits=4)

    class Meta:
        ordering = ('-date', 'emp__id', 'app__id', 'task__type', 'defect__id', 'adhoc__id')

    def __str__(self):
        return str('Employee: ' + str(self.emp) + ' App: ' + str(self.app) + ' Task: ' + str(self.task) + ' Defect: '
                   + str(self.defect) + ' Adhoc: ' + str(self.adhoc) + ' Hours: ' + str(self.hours))


class TimesheetForm(ModelForm):
    """Input form for Timesheet data entry by user"""
    class Meta:
        model = Timesheet
        fields = ['emp', 'app', 'task', 'defect', 'adhoc', 'date', 'hours']

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('task')
        adhoc = cleaned_data.get('adhoc')
        defect = cleaned_data.get('defect')

        if task.type == 'Adhoc' and adhoc is None:
            self.fields['adhoc'].required = True
            raise ValidationError("Adhoc item is required")
        elif task.type == 'Defect' and defect is None:
            self.fields['defect'].required = True
            raise ValidationError("Defect item is required")
        elif adhoc is not None and task.type != 'Adhoc':
            raise ValidationError("Adhoc requires matching Task")
        elif defect is not None and task.type != 'Defect':
            raise ValidationError("Defect requires matching Task")
        return cleaned_data

