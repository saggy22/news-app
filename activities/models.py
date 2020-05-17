from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from wuchna.utils.models import TimeStampedModel
from pages.exceptions import AlreadyExistsError

User = get_user_model()


# Create your models here.
class Activity(TimeStampedModel):
    """

    """
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Upvote'),
        (DOWN_VOTE, 'Downvote'),
    )

    user = models.ForeignKey(User, related_name='activity', on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    # Mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()

