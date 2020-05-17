"""Wuchna URL Configuration
"""
from django.urls import path, include, re_path

from activities.views import *

urlpatterns = [
    path('perform-action/<str:page>', perform_action, name="perform_action"),
]
