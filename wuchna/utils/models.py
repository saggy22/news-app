from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    """
    This mixins provide the default field in the models project wise
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_updated", on_delete=models.CASCADE)

    class Meta:
        abstract = True

