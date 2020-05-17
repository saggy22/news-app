from django.urls import path, re_path
from rest_framework import routers

from . import views
from .api_views import *
#from .api_views import FollowPageViewSet, PagesQuestionViewSet

router = routers.DefaultRouter()
router.register(r'follow-page', FollowPageViewSet)
#router.register('question-api', PagesQuestionViewSet, base_name='question-api')

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('p/<str:name>/', views.ContentPage.as_view(), name='page'),
    path('default/', views.DefaultPage.as_view(), name='default_page'),
    path('follower/<str:page>/', views.followers, name='page_followers'),
    path('following/', views.following, name='pages_following'),
   	path('add-follower/<str:page>/', views.add_follower, name='add_page_follower'),
    #re_path(r'add-follower/(?P<page>\w+)/$', views.add_follower, name='add_page_follower'),
    path('remove-follower/<str:page>/', views.remove_follower, name='remove_page_follower'),
    path('ask-question/<str:page>/', views.ask_question, name='ask_question'),
    path('give-answer/<str:page>/', views.give_answer, name='give_answer'),
    path('post-comment/<str:page>/', views.post_comment, name='post_comment'),    
    path('pages-question/<str:page>/', views.pages_question, name='pages_question'),
    path('pages-answer/<str:page>/<str:question>/', views.pages_answer, name='pages_answer'),
    path('pages-comment/<str:page>/', views.pages_comment, name='pages_comment'),
    path('delete-pages-comment/<str:page>/', views.delete_pages_comment, name='delete_pages_comment'),
]

urlpatterns += router.urls