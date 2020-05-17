import hashlib
import random
import string
import time
import logging

from rest_framework import serializers

from django.contrib.auth.models import AnonymousUser, Group
from django.contrib.auth import get_user_model

from django.conf import settings
from django.db import transaction
from django.db.models import Max

from .models import UserProfile


User = get_user_model()


#register with username/email
class UserProfileSerializer(serializers.ModelSerializer):
	username = serializers.CharField(write_only=True)
	email = serializers.CharField(write_only=True)
	password = serializers.CharField(write_only=True)
	time_zone = serializers.SerializerMethodField()

	class Meta:
		model = UserProfile
		#fields = '__all__'
		exclude = ['user', 'created_by', 'updated_by', 'gender']

	def get_time_zone(self, obj):
		if obj.time_zone is not None:
			return obj.time_zone.__str__()
		else:
			return ''

	def validate(self, data):
		initial_data = self.initial_data
		required_fields = ['phone','location','dob','language','profession']
		for field in required_fields:
			  field_value = initial_data.get(field, None)
			  if not field_value:
				  raise serializers.ValidationError('%s field is required'%(field))
				  break
		return initial_data     


	def create(self, validated_data):
		with transaction.atomic():
			#import pdb; pdb.set_trace()
			username = validated_data['username']
			email = validated_data['email']
			password = validated_data['password']
			user = User.objects.create(username=username, email=email)
			user.set_password(password)
			user.save()

			# add remaining fields
			if 'gender' in validated_data.keys():
				gender = validated_data['gender']
			else :
				gender = 0

			if 'phone' in validated_data.keys():
				phone = validated_data['phone']	

			if 'location' in validated_data.keys():
				location = validated_data['location']

			if 'dob' in validated_data.keys():
				dob = validated_data['dob']

			if 'language' in validated_data.keys():
				language = validated_data['language']

			if 'profession' in validated_data.keys():
				profession = validated_data['profession']									

			user_profile = UserProfile.objects.create(
					user = user,
		            phone = phone,
		            location = location,
		            language = language,
		            dob = dob,
		            gender = gender,
		            profession = profession,
		            created_by = user,
					updated_by = user
		        )

			return user_profile