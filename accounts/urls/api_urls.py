"""millers URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import api_views as views

router = DefaultRouter()

urlpatterns = [
		#path(r'^login-api/', views.UserLoginView.as_view()),
		]