from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow


@receiver(post_save,sender=User)
def user_create_follow(sender,instance:User,created,**kwargs):
    if created:
        Follow.objects.create(to_user=instance)


# @receiver(post_save,sender=Blog)
# def message_to_followers_newBlog(sender,instance:Blog,created,**kwargs):
#     if created:
#         author = instance.author
#         followers = author.follow.followers.all().values_list("username",flat=True)
#         print(followers)