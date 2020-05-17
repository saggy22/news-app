from django.urls import path

from . import views

urlpatterns = [   
    path('page/<str:name>/', views.ContentResearchPage.as_view(), name='research-page'),
    #path('default/', views.DefaultPage.as_view(), name='default_page'),
]
