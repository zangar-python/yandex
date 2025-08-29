from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import File

@receiver(post_delete,sender=File)
def delete_file_if_model_deleted(sender,instance:File,**kwargs):
    if instance.file:
        instance.file.delete(False)