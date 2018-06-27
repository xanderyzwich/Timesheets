from django.urls import path

from . import views

app_name = 'timesheets'
urlpatterns = [
    path('', views.index, name='index'),
    path('apps/', views.apps, name='apps'),
    path('app/<int:app_id>/', views.app, name='app'),
]