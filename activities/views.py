from django.shortcuts import render, redirect
from activities.models import Activity
from pages.models import PagesQuestion, PagesAnswer, PagesComment 

# return upvote/ downvote result
def perform_action(request, page):
	#take input 	
	try:
		if request.post['object'] == "question":
			question = PagesQuestion.objects.get(id=request.POST['id'])
			content_object = question

		elif request.post['object'] == "answer":
			answer = PagesAnswer.objects.get(id=request.POST['id'])
			content_object = answer

		elif request.post['object'] == "comment":
			comment = PagesComment.objects.get(id=request.POST['id'])
			content_object = comment			

		if Activity.objects.filter(content_object=content_object, user=request.user).exists():
			activity = Activity.objects.get(content_object=question, user=request.user)
			activity.activity_type = request.POST['activity_type']
			activity.save()
		else:
			Activity.objects.create(content_object=content_object, user=request.user)
	except Exception as e:
		print (e)	
	redirect("/p/%s"%(page))
