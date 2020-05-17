from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from wuchna.utils.models import TimeStampedModel
from pages.exceptions import AlreadyExistsError
from activities.models import Activity

User = get_user_model()


class PagesComment(TimeStampedModel):
    """

    """
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    comment = models.TextField()
    published = models.BooleanField(default=False)
    votes = GenericRelation(Activity)


class PagesQuestion(TimeStampedModel):
    """

    """
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    question = models.TextField()
    published = models.BooleanField(default=False)
    votes = GenericRelation(Activity)

    def __str__(self):
        if len(self.question)>255:
            return "%s"%(self.question[:255])
        else: 
            return "%s"%(self.question)

    class Meta:
        unique_together = (("page", "question"),)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    @property
    def url(self):
        return "/questions/{}".format(self.pk)


class PagesAnswer(TimeStampedModel):
    """

    """
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(PagesQuestion, related_name='answers', on_delete=models.CASCADE)
    page = models.CharField(max_length=255)
    answer = models.TextField()
    published = models.BooleanField(default=False)
    votes = GenericRelation(Activity)

    class Meta:
        unique_together = (('question', 'answer'),)

    def __str__(self):
        if len(self.answer)>255:
            return "%s"%(self.answer[:255])
        else: 
            return "%s"%(self.answer)

    def publish(self):
        answers = Answer.objects.filter(question=self.question)
        for answer in answers:
            answers.published = False
            answer.save()
        self.published = True   
        self.save()



class FollowPageManager(models.Manager):

    def followers(self, url):
        """ returns the list of followers of a page  """
        qs = FollowPage.objects.filter(url=url)
        users = [item.user for item in qs]
        return users

    def following(self, user):
        """ returns the list of pags a user is following """
        qs = FollowPage.objects.filter(user=user)
        urls = [item.url for item in qs]
        return urls    

    def add_follower(self, user, url):
        """ add user as a follower of a page """
        relation, created = FollowPage.objects.get_or_create(user=user, url=url, created_by=user, updated_by=user)
        if created:
            raise AlreadyExistsError("User '%s' already follows '%s'"%(user,url))
        return relation

    def remove_follow(self, user, url):    
        """ remove a user as a follower of a page  """
        try:
            qs = FollowPage.objects.get(user=user, url=url)
            qs.delete()
            return True
        except FollowPage.DoesNotExist:
            return False

    def is_following(self, user, url):    
        """ check if a user follows a topic/page  """
        try:
            qs = FollowPage.objects.get(user=user, url=url)
            return True
        except FollowPage.DoesNotExist:
            return False


class FollowPage(TimeStampedModel):
    user = models.ForeignKey(User, related_name='user_following_page', on_delete=models.CASCADE)
    url = models.CharField(max_length=250, null=True, blank=True)
    objects = FollowPageManager()

    class Meta:
        unique_together = (("user", "url"),)

    def __str__(self):
        return  "User #%s follows Page#%s"%(self.user, self.url)
