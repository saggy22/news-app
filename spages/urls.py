from django.urls import path

from spages import views

urlpatterns = [
	path('terms-n-conditions/', views.TermsNConditionsPage.as_view(), name='terms-and-conditions'),
	path('policy/', views.PolicyPage.as_view(), name='policy-page'),
]