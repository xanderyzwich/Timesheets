# Timesheets
Depends on django and pytz

Timesheets is an internal team utility for tracking time spent on application support activities in an effort to better project and balance labor efforts.



index.html
This template allows for time sheet submission, and is utilized as the primary landing page.

timesheet.html
This template is used for listing of time entries. The default usage at /timesheets/report lists entries for the current month. It is used by entry specific pages for Adhoc, App, Defect, Employee, and Task models. There are also multiple url formats for fetching data by year, month or year via /timesheet/report/[year]/[month]/[day].

list.html
This is used for ease of navigating to all specific entry pages in of the various models by way of /timesheet/[model] or [model]s .
