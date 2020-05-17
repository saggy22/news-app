# -*- coding: utf-8 -*-
import json

from django.http import Http404, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
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


from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import mixins, generics, viewsets, exceptions, \
authentication, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from accounts.data_wrapper import data_wrapper_response


from .models import UserProfile
from .forms import UserProfileForm


class ProfileCurrentUserView(TemplateView):
	template_name = 'accounts/user_profile.html'

	def dispatch(self, *args, **kwargs):
		return super(ProfileCurrentUserView, self).dispatch(*args, **kwargs)

	# def context(self, *args, **kwargs):
	# 	context = super(ProfileCurrentUserView, self).context(*args, **kwargs)
	# 	user = UserProfile.objects.get(id=kwargs['user_id'])
	# 	context['user'] = user
	# 	return context

	def get(self, request, *args, **kwargs):
		try:      
			#context = self.get_context_data()   
			context = {}
			user = UserProfile.objects.get(id=kwargs['user_id'])
			context['user'] = user
			template = loader.get_template('accounts/user_profile.html')            
			return render(request, 'accounts/user_profile.html', context)
			
		except Exception as e:
			return HttpResponse(e)  

	def post(self, request, *args, **kwargs):
		try:
			context = {}
			user = UserProfile.objects.get(id=kwargs['user_id'])
			#import pdb; pdb.set_trace()
			form = UserProfileForm(request.POST, instance=user)
			if form.is_valid():
				form.save()
			user = UserProfile.objects.get(id=kwargs['user_id'])
			context['user'] = user
			template = loader.get_template('accounts/user_profile.html')
			return HttpResponse(template.render(context, request))
	  
		except Exception as e:
			return HttpResponse(e)