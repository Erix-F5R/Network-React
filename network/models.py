from email.headerregistry import ContentTransferEncodingHeader
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user} {self.date}"

    def serialize(self):
        return {
            "username": self.user.get_username(),
            "body": self.body,
            "date": self.date

        }

class Follower(models.Model):
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
       return f"{self.following} follows {self.followed}"

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes a post by: {self.post}"