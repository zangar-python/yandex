from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blogs")
    # likes = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes",null=True,blank=True)
    
    likes = models.ManyToManyField(User,related_name="liked_blogs",null=True,blank=True)
    
    header = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/",blank=True,null=True)    
    public = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.header}"

class Blocks(models.Model):
    header = models.TextField(max_length=50)
    title = models.TextField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="blocks")
    image = models.ImageField(upload_to="images/",blank=True,null=True) 
    def __str__(self):
        return f"to : {self.blog.header}"
    
class Comment(models.Model):
    to_blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="comments")
    text = models.CharField(max_length=250)
    user = models.ForeignKey(User,models.CASCADE,related_name="comments")
    likes = models.ManyToManyField(User,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def likes_count(self):
        return self.likes.count()
    def __str__(self):
        return self.text
    