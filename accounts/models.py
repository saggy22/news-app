from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from languages.fields import LanguageField
from timezone_field import TimeZoneField
from versatileimagefield.fields import VersatileImageField

from wuchna.utils.models import TimeStampedModel

# from generic_follow.model_mixins import UserFollowMixin


User = get_user_model()

GENDER = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Other'),
)

INTERESTS = (
    (0, 'Entertainment'),
    (1, 'Science'),
)


class UserProfile(TimeStampedModel):
    """

    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    tag = models.CharField(max_length=120, blank=True, null=True)
    picture = VersatileImageField(upload_to='profile', blank=True, null=True)
    aboutme = models.TextField(blank=True, null=True, verbose_name="Profile Summary")
    phone = models.CharField(max_length=120, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    time_zone = TimeZoneField(default='Asia/Kolkata', null=True, blank=True)
    language = LanguageField(default='en')
    dob = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER)

    class Meta:
        ordering = ("-date_updated",)

    def __str__(self):
        """

        :return:
        """
        return "Profile of {}".format(self.user.get_full_name())

    @property
    def get_location(self):
        return "{}".format(self.location)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'userid': self.user.username})

    def get_screen_name(self):
        return "{}".format(self.user.get_full_name())

    @property
    def get_picture(self):
        if not self.picture:
            self.picture = 'placeholder/no-image.png'
            self.save()
        return self.picture


class UserInterests(TimeStampedModel):
    """

    """
    user = models.OneToOneField(User, related_name='interests', on_delete=models.CASCADE)
    interest = models.PositiveSmallIntegerField(choices=INTERESTS)


class TempPages(models.Model):
    """

    """
    url = models.TextField(blank=True, null=True)
