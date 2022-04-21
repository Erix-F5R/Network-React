from django.contrib import admin
from .models import Follower, User, Post, Like
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)