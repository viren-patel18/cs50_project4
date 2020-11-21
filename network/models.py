from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, related_name="users")
    followers = models.ManyToManyField("self", blank=True, related_name="users")

class Post(models.Model):
    content = models.CharField(max_length=3000)
    ts = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likedBy = models.ManyToManyField(User, blank=True, null=True, related_name="likes")
