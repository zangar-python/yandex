from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Blog

@receiver(post_delete,sender=Blog)
def delete_file_on_blog_delete(sender,instance:Blog,**kwargs):
    if instance.image:
        instance.image.delete(False)
