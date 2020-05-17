from django import template
from django.contrib.contenttypes.models import ContentType

from pages.models import FollowPage
from activities.models import Activity

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

register = template.Library()


# it tells the count for upvote and downvote for an question, answer, comment
@register.simple_tag
def activity_count_questions(question, activity_type):
    import pdb; pdb.set_trace()
    # Pass the instance we created in the snippet above
    count = question.votes.filter(activity_type="U").count()
    return count
