from django.contrib import admin
from .models import UserProfile, TempPages

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TempPages)
