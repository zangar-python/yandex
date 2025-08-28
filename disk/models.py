from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class File(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="saved_files")
    file = models.FileField(upload_to="files")
    
    def __str__(self):
        return f"{self.user} {self.title}"