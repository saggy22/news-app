from django import forms
from .models import PagesQuestion, PagesAnswer, PagesComment


class PagesQuestionForm(forms.ModelForm):
	class Meta:
		model = PagesQuestion
		exclude = ('created_by', 'updated_by')


class PagesAnswerForm(forms.ModelForm):
	class Meta:
		model = PagesAnswer
		exclude = ('created_by', 'updated_by')


class PagesCommentForm(forms.ModelForm):
	class Meta:
		model = PagesComment
		exclude = ('created_by', 'updated_by')		