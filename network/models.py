from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = False
    
