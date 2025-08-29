from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Follow(models.Model):
    to_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="follow")
    followers = models.ManyToManyField(User,related_name="followings",blank=True)
    