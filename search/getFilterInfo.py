from django.contrib.auth.models import User
from news.models import Blog
# from django.db.models import Count
# from accounts.models import Follow
# from news.serializers import BlocksSerializer

def getUserObject(user:User):
    followers = user.follow.followers.all()
    count_followers = followers.count()
    count_followings = user.followings.all().count()
    obj = {
        "username":user.username,
        "id":user.id,
        "count_followers":count_followers,
        "count_followings":count_followings
    }
    return obj

def blogGetObject(blog:Blog):
    likes = blog.likes.all().count()
    obj = {
        "header":blog.header,
        "likes":likes,
        "author":blog.author.id,
        "id":blog.id
    }
    return obj

def GetObjects(users,blogs):
    users_new = []
    for user in users:   
        users_new.append(getUserObject(user))
    blogs_new = []
    for blog in blogs:
        blogs_new.append(blogGetObject(blog))
    return {
        "users":users_new,
        "blogs":blogs_new
    }