"""millers URL Configuration
"""
from django.urls import path, include, re_path

from accounts.views import *
from accounts.api_views import *


urlpatterns = [
    path('', include('allauth.urls')),
    re_path(r'^profile/(?P<user_id>\d+)/$', ProfileCurrentUserView.as_view(), name='user_profile'),
    path('login-api/', UserLoginView.as_view()),
    path('signup-api/', UserSignupView.as_view()),
    re_path(r'^reset-password-api/(?P<pk>\d+)/$', ResetPasswordView.as_view()),
    re_path(r'^forgot-password-api/(?P<pk>\d+)/$', ForgotPasswordView.as_view()),
    # path('avatar_upload/', uploadAvatar, name='upload_avatar'),
    # path('profile/<str:userid>/', ProfileView.as_view(), name='user_profile'),
    # path('profile/', ProfileCurrentUserView.as_view(), name='mentor_profile'),
    # path('projects/', MyProjects.as_view(), name='my_projects'),
    # path('settings/', SettingsView.as_view(), name='setting'),
]
