import requests
import sys
import traceback

from django.http import Http404, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework import routers, serializers, viewsets
from django_filters import rest_framework as filters
from django.contrib.auth.models import AnonymousUser


from .models import PagesModel, FollowPage, PagesQuestion, PagesAnswer,\
PagesComment
from .exceptions import AlreadyExistsError
from .forms import PagesQuestionForm, PagesAnswerForm, PagesCommentForm
from .serializers import FollowPageSerializer, PagesQuestionSerializer
from .filters import PagesQuestionFilter

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User
from .models import PagesModel


class ContentPage(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        name = kwargs.get('name')
        page = name.lower()
        if name and '_' in name or any(x.isupper() for x in name):
            name = name.replace('_', '-')
            ctx['redirect'] = name.lower()
        else:
            try:
                ctx['m'] = PagesModel.objects.get(url=kwargs.get('name').lower())
            except PagesModel.DoesNotExist:
                raise Http404
        ctx['colorsarray'] = ['primary', 'info', 'danger', 'success', 'warning']
        ctx['page'] = page
        ctx['questions'] = pages_question(page)
        ctx['comments'] = pages_comment(page)#.filter(published=True)
        #ctx['comments_pending'] = pages_comment(page).filter(published=False)

        return ctx

    def render_to_response(self, context, **response_kwargs):
        if context.get('redirect', None):
            return redirect('page', name=context.get('redirect'), permanent=True)
        return super().render_to_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        try:
            ctx = self.get_context_data(**kwargs)
            if not isinstance(request.user, AnonymousUser):   
               ctx['follow'] = FollowPage.objects.is_following(request.user, ctx['page'])

            return render(request, 'pages/index.html', ctx)

        except Exception as e:
            print (traceback.format_exc(sys.exc_info()))
            return HttpResponse(e)


class HomePage(TemplateView):
    template_name = 'pages/homepage.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['url'] = kwargs.get('name')
        return ctx


class AboutPage(TemplateView):
    template_name = 'pages/about.html'

    def get_content_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['url'] = kwargs.get('name')
        return ctx


class DefaultPage(TemplateView):
    template_name = 'pages/default.html'


def followers(request, page, template_name='pages/follow/followers_list.html'):
    """ Returns all followers of a page """
    users = FollowPage.objects.followers(page)
    ctx = {"users":users}
    return render(request, template_name, ctx)


def following(request, template_name='pages/follow/following_list.html'):
    """ Returns all pages a user is following  """
    user = request.user
    pages = FollowPage.objects.following(user)
    ctx = {"pages":pages}
    return render(request, template_name, ctx)


def add_follower(request, page):
    """ Add a user as a follower of a page """
    ctx = {}
    follower = request.user
    try:
        qs = FollowPage.objects.add_follower(follower, page)
    except Exception as e:
        ctx["error"] = e
    return redirect("/p/%s/"%(page))


def remove_follower(request, page):
    """ Removes a user as a follower of a page """
    ctx = {}
    user = request.user
    try:
        qs = FollowPage.objects.remove_follow(user, page)
    except FollowPage.DoesNotExist as e:
        ctx['error'] = e
    return redirect("/p/%s/"%(page))


def pages_question(page):
    """ Returns all questions related to a page """
    questions = PagesQuestion.objects.filter(page=page)
    return questions


@login_required
def ask_question(request, page):
    ctx = {}
    # validate the form and save using the form
    form = PagesQuestionForm(request.POST)
    if form.is_valid():
        PagesQuestion = form.save(commit=False)
        PagesQuestion.created_by = request.user
        PagesQuestion.updated_by = request.user
        PagesQuestion = PagesQuestion.save()
    return redirect("/p/%s/"%(page))    


def pages_answer(question, page):
    """ Returns all questions related to a page """
    answers = PagesAnswer.objects.filter(question=question, page=page)
    return answers


@login_required
def give_answer(request, page):
    ctx = {}
    # validate the form and save using the form
    form = PagesAnswerForm(request.POST)
    if form.is_valid():
        PagesAnswer = form.save(commit=False)
        PagesAnswer.created_by = request.user
        PagesAnswer.updated_by = request.user
        PagesAnswer = PagesAnswer.save()

    return redirect("/p/%s/"%(page))


def pages_comment(page):
    """ Returns all comment related to a page """
    comments = PagesComment.objects.filter(page=page)
    return comments


@login_required
def post_comment(request, page):
    ctx = {}
    # validate the form and save using the form
    form = PagesCommentForm(request.POST)
    if form.is_valid():
        PagesComment = form.save(commit=False)
        PagesComment.created_by = request.user
        PagesComment.updated_by = request.user
        PagesComment = PagesComment.save()

    return redirect("/p/%s/"%(page))


@login_required
def delete_pages_comment(request, page):
    """ Delete the comment related to a page """
    comments = PagesComment.objects.filter(id=int(request.POST['id'])).delete()
    return redirect("/p/%s/"%(page))    
