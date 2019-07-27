# -*- coding: utf-8 -*-

from django.urls import path, include
from . import views

app_name = 'worktracker'

urlpatterns = [
    path('', views.control, name='control'),
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
    path('client-report/', views.report, name='client-report'),
    path('project-report/', views.reportproject, name='project-report')
]
