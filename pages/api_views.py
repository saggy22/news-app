# -*- coding: utf-8 -*-
import json
import traceback
import sys
import string
import time
import hashlib
import random

from django.http import Http404, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render, redirect, get_list_or_404, get_object_or_404
from django.views.generic import TemplateView
from django.template import loader
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.files import File
from django.db.models.aggregates import Sum
from django.db.models import Q
from django.contrib.auth import logout
from django_filters import rest_framework as filters

from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import mixins, generics, viewsets, exceptions, \
authentication, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from common.data_wrapper import data_wrapper_response, format_data
from common.views import DataWrapperViewSet

from .models import FollowPage, PagesQuestion
from .serializers import FollowPageSerializer, PagesQuestionSerializer
from .filters import PagesQuestionFilter
#from accounts.data_wrapper import GenericDataWrapper


class FollowPageViewSet(DataWrapperViewSet):
	'''
	This class handles all operation of import history of uploads.
	Methods:
		Update:PUT
		Create:POST
		List:GET,
		Retrieve: GET(with pk(id) of object in url)
		Delete:Delete
	'''
	model = FollowPage
	queryset = FollowPage.objects.all()
	serializer_class = FollowPageSerializer
	# filter_backends = (filters.DjangoFilterBackend,)
	# filter_class = FollowPageFilter



class PagesQuestionViewSet(viewsets.ViewSet):
	""" This class handles all operations of questions related to a page """
	model = PagesQuestion
	queryset = PagesQuestion.objects.all()
	serializer_class = PagesQuestionSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_class = PagesQuestionFilter
