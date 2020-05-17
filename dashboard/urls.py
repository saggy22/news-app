from django.urls import path

from . import views


urlpatterns = [
    path('', views.DashBoardIndex.as_view(), name='dashboard'),
    path('page/', views.PageListView.as_view(), name='pages_list'),
    path('pageedit/<str:name>/', views.PageEditView.as_view(), name='pages_edit'),
    path('research-page/', views.ResearchPageListView.as_view(), name='research_pages_list'),
    path('research-pageedit/<str:name>/', views.ResearchPageEditView.as_view(), name='research_pages_edit'),
]
