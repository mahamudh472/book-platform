from django.contrib import admin
from .models import UserProfile, UserFollow
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserFollow)
