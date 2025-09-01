from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser


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
            return Response(data={
                'username':user.username,
                "password":user.password,
                "id":user.id,
                "connect":True,
                "user_saved":True
                },status=status.HTTP_200_OK)
        return Response(data={
            "error":serializer.data,
            "detail":{
                "connect":False,
                "user_saved":False
            }
        },status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self,request:Request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request,username=username,password=password)
        if not user:
            return Response(data={
                "error":"Пользователья с такими данными не существует"    
                },status=status.HTTP_404_NOT_FOUND)
            
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
                "user_posts":user_blogs_serializer.data
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

class GetAllUserData(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request:Request):
        users = User.objects.all().exclude(is_superuser=True)
        users_serializer = UserSerializer(users,many=True)
        users_follow = [f.follow for f in users]
        follow_serializer = FollowSerializer(users_follow,many=True)
        
        return Response(data={
            "users":users_serializer.data,
            "user_follow":follow_serializer.data
        })