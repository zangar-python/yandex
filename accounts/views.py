from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from rest_framework import status
from .serializer import UserSerializer

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
    