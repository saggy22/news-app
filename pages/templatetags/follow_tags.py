from django import template

from pages.models import FollowPage

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

register = template.Library()

# it tells if a user is following a page
#@register.inclusion_tag('pages/templatetags/followButton.html')
@register.tag
def followButton(user, page):
    ctx = {'following':False, 'user':user, 'page':page}
    try:
        fObj = FollowPage.objects.get(user=user, page=page)
        ctx['following'] = True
        ctx['obj'] = fObj
    except FollowPage.DoesNotExist:
        pass
    return {'ctx': ctx}
