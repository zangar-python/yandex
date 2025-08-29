from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework import status
from .serializer import UserSerializer,User,FollowSerializer

from news.serializers import BlogSerializer


class UserRegisterView(APIView):
    def post(self,request:Request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username':user.username,"password":user.password,"id":user.id})
        return Response(serializer.errors)
    
class UserLoginView(APIView):
    def post(self,request:Request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request,username=username,password=password)
        if not user:
            return Response("Неправильные данные",status.HTTP_400_BAD_REQUEST)
        token,created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key})
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request:Request):
        user = request.user
        user_blogs = user.blogs.all()
        user_blogs_serializer = BlogSerializer(user_blogs,many=True)
        return Response(
            {
                "username":user.username,
                "id":user.id,
                "your_posts":user_blogs_serializer.data
            }
        )

class UserLikedBlogs(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request):
        user = request.user
        
        liked_blogs = user.liked_blogs.all()
        serializator = BlogSerializer(liked_blogs,many=True)
        return Response(
            {
                "username":user.username,
                "id":user.id,
                "liked_blogs":serializator.data 
            }
        )    
    
class UserFollowing(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request,pk):
        user_to_follow = get_object_or_404(User,pk=pk)
        follow =  user_to_follow.follow
        followed = request.user in follow.followers.all()
        if followed:
            follow.followers.remove(request.user)
            res = f"removed follow from {user_to_follow.username}"
        else:
            follow.followers.add(request.user)
            res = f"followed to user {user_to_follow}"
        return Response(data={
            "user":request.user.username,
            "result":res,
        })
class UserFollowers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,requests:Request):
        user = requests.user
        
        serializer = FollowSerializer(user.follow)
        return Response(
            data={
                "follow":serializer.data,
                "username":user.username
            }
        )

class UserFollowings(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request):
        user = request.user
        followings = user.followings.all().values_list("to_user",flat=True)
        # serializer = FollowSerializer(followings)
        return Response({
            "user":user.id,
            "username":user.username,
            "followings":followings
        })
        