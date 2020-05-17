from django.contrib import admin
from .models import FollowPage, PagesQuestion, PagesAnswer

# Register your models here.
admin.site.register(FollowPage)
admin.site.register(PagesQuestion)
admin.site.register(PagesAnswer)
