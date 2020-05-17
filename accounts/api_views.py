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

from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import mixins, generics, viewsets, exceptions, \
authentication, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from accounts.data_wrapper import data_wrapper_response, format_data

from .models import UserProfile
from .serializers import UserProfileSerializer
#from accounts.data_wrapper import GenericDataWrapper


'''
This class is to manipulate data for generic api views 
as per Android requirements before returning data
createdby :Sagar

Developer needs to extend this class to use its functionalities
'''
class GenericDataWrapper(object):

	def dispatch(self, *args, **kwargs):
		result =  super(GenericDataWrapper, self).dispatch(*args, **kwargs)
		data = format_data(result)      
		return data



class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening



chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
def password_generator(length=8):
	return ''.join(random.choice(chars) for i in range(length))


def generate_token(email):
	ts = str(time.time())
	salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
	activation_key = hashlib.sha1(salt+email+ts).hexdigest()
	return activation_key


#basic signup functionality
class UserSignupView(GenericDataWrapper, generics.ListCreateAPIView):
	model = UserProfile
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer



#basic login functionlaity with exception handling
class UserLoginView(APIView):

	def post(self, request):
		data = {}
		data['message'] = False

		try:
			#import pdb; pdb.set_trace()

			username = request.data.get('username', None)
			password = request.data.get('password', None)
	 
			if not username or not password:
				raise exceptions.AuthenticationFailed('Username or passsword not provided.')
	 
			credentials = {
				'username': username,
				'password': password
			}
	 
			user = authenticate(**credentials)

			if user is None:   
				raise exceptions.AuthenticationFailed('Invalid username/password.')
			
			login(request, user)               
			request.session.set_expiry(settings.SESSION_TIMEOUT)
			#token, created = Token.objects.get_or_create(user=user)

			data['message'] = "Login Successful"
			#data['token'] = token

			return data_wrapper_response(data=data, status_code=200)
		except Exception as e:
			if str(e) == "Username or passsword not provided." or str(e) == "Invalid username/password.":
				data['message'] = str(e)
				return data_wrapper_response(data=data, status_code=200)    
			data['message']=str(e)
			return data_wrapper_response(data=data, status_code=500)



'''
This class reset the account password.
Created By: Sagar
'''
class ResetPasswordView(APIView):
 
	model = User

	def post(self, request, *args, **kwargs):
		
		response_data = {}
		try:
			import pdb; pdb.set_trace()
			old_password = request.data.get('old_password')
			new_password = request.data.get('new_password')
			if User.objects.filter(id=kwargs['pk']).exists():
				user = User.objects.get(id=kwargs['pk'])
				if not user.check_password(old_password):
					response_data['message'] = "Old password do not match."
					return data_wrapper_response(data=response_data,status_code=200)
				user.set_password(new_password)
				user.save()
				username = user.username
				credentials = {
						'username': username,
						'password': new_password
					}
			 
				user = authenticate(request, **credentials)
				request.session.set_expiry(settings.SESSION_TIMEOUT)
				login(request, user)
				response_data['message'] = "Password reset successful."
			else:
				response_data['message'] = "This account doesn't exist anymore."
			return data_wrapper_response(data=response_data,status_code=200)
		except Exception as e:
			#logging.info("Class name: %s - Error = %s:"%('ResetPassword View',str(e)))
			#logging.info(traceback.format_exc(sys.exc_info()))
			print (traceback.format_exc(sys.exc_info()))
			response_data['message'] = str(e)
			return data_wrapper_response(data=response_data,status_code=500)


'''
This class reset the account password and sends the activation mail
Created By: Sagar
'''
class ForgotPasswordView(APIView):
 
    model = User
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        
        response_data = {}
        try:
            #email = request.data.get('email')
            #import pdb; pdb.set_trace()
            if User.objects.filter(id=kwargs['pk']).exists():
                user = User.objects.get(id=kwargs['pk'])
                
                #generate a random password
                password = password_generator(settings.PASSWORD_LENGTH)
                user.set_password(password)
                user.save()

                #generate activation key
                email = user.email
                activation_key = generate_token(email)
                user_profile = UserProfile.objects.get(user=user)
                user_profile.activation_key = activation_key
                user_profile.save()                

                response_data['message'] = True
            else:
                response_data['message'] = False
            return data_wrapper_response(data=response_data,status_code=200)
        except Exception as e:
            # logging.info("Class name: %s - Error = %s:"%('ForgotPassword View',str(e)))
            # logging.info(traceback.format_exc(sys.exc_info()))
            print (traceback.format_exc(sys.exc_info()))
            response_data['message'] = str(e)
            return data_wrapper_response(data=response_data,status_code=500)