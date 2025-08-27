from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    header = models.CharField(max_length=50)
    text = models.TextField()
    sended = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_me")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="to_me")
    is_readed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"from:{self.from_user}"
    
    