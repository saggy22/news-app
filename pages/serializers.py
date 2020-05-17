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

from .models import FollowPage, PagesQuestion, PagesAnswer

User = get_user_model()


#follow page serializer
class FollowPageSerializer(serializers.ModelSerializer):

	class Meta:
		model = FollowPage
		fields = '__all__'


#question serializer to return questions and related answers
class PagesQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = PagesQuestion
        fields = "__all__"