"""
URL configuration for sendcloud project.
"""

from django.urls import path

from sendcloud_assignment.api import api

urlpatterns = [path("", api.urls)]
