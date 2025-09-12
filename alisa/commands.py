from django.contrib.auth.models import User
from accounts.serializer import UserSerializer
from accounts.models import Follow

from news.models import Blog
from news.serializers import BlogSerializer

from .commands_ import commands

class AlisaMethods():
    def __init__(self,user:User):
        self.user = user
        pass
    alisa_commands = commands
    
    def construct_data(self,data):
        return {
            "username":self.user.username,
            "id":self.user.id,
            "data":data,
        }
    
    def command(self,command:str):
        if "find_user/" in command:
            if len(command.split("/")) != 2:
                return self.err_400_BAD_REQUEST() 
            username = command.split("/")[1]
            return self.findUsers(username)
        if "find_blog/" in command:
            if len(command.split("/")) != 2:
                return self.err_400_BAD_REQUEST() 
            blog_header = command.split("/")[1]
            return self.findBlogs(blog_header)
        if command.lower() == "hello":
            return self.send_hello()
        if command.lower() == "my_account":
            return self.my_account()
        if command.lower() == "help":
            return self.help_commands()
        else:
            return self.err_400_BAD_REQUEST()
    
    def findUsers(self,username):
        users = User.objects.filter(
            username__icontains=username
        )[:10]
        users_serializer = UserSerializer(users,many=True)
        return self.construct_data(users_serializer.data)

    def findBlogs(self,blog_header):
        blogs = Blog.objects.filter(
            header__icontains=blog_header
        )[:10]
        blogs_serializer = BlogSerializer(blogs,many=True)
        return self.construct_data(blogs_serializer.data)
    
    def send_hello(self):
        data = {
            "msg":f"Hello {self.user.username}!Can I help for you?You need help,type 'help'."
        }
        return self.construct_data(data)
    
    def my_account(self):
        data = {
            "info":{
                "username":self.user.username,
                "id":self.user.id,
            },
            "follow":{
                "followers_count":self.user.follow.followers.count(),
                "followings_count":self.user.followings.count()
            }
        }
        return self.construct_data(data)
    
    def help_commands(self):
        return self.construct_data(self.alisa_commands)
    
    def err_400_BAD_REQUEST(self):
        data = {
            "error":"Error message,command is not variable",
            "command_code":"400 BAD-REQUEST"
        }
        return self.construct_data(data)