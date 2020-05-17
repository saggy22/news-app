from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class TermsNConditionsPage(TemplateView):
	template_name = 'spages/terms-n-conditions.html'


class PolicyPage(TemplateView):
	template_name = 'spages/policy.html'	
