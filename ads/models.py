from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ad(models.Model):
    img = models.ImageField(upload_to="images/")
    header = models.CharField(max_length=120)
    text = models.TextField()
    to_link = models.URLField()
    author = models.ForeignKey(User,models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.header