from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render

User = get_user_model()

'''
For Generic 404 error
Created By: Sagar Bhatia
'''


def error_404(request):
    '''
    It is 404 customize page.
    Use this method with handler if we need to customize page from backend.
    '''
    data = {}
    return render(request, 'common/404.html', data)


# set data on redis on system startup
def load_on_startup():
    # load list of users
    users = User.objects.all()
    # replace this by group_by queries
    # for user in users:
    #     list_topics_followed = Follow.objects.filter(user=user).values_list('target_temppages')
    #     cache.set(user.id, list_topics_followed)

# Follow.objects.all().group_by('user').values_list('objects')
