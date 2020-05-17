from django_filters import rest_framework as filters
from .models import PagesQuestion, PagesAnswer


class PagesQuestionFilter(filters.FilterSet):
	'''
	Filter class for questions
	'''
	class Meta:
	    model = PagesQuestion
	    fields = '__all__'


class PagesAnswerFilter(filters.FilterSet):
	'''
	Filter class for answers
	'''
	class Meta:
	    model = PagesAnswer
	    fields = '__all__'
