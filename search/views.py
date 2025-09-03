from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from news.models import Blog,Blocks
from django.db.models import Count
from accounts.serializer import UserSerializer
from news.serializers import BlogSerializer,BlocksSerializer

from .getFilterInfo import GetObjects

class FilterGet(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request,word:str):
        users = User.objects.filter(username__contains=word).exclude(is_superuser=True)
        blogs = Blog.objects.filter(header__contains=word).exclude(public=False).annotate(like_sum=Count("likes")).order_by("-like_sum")
        not_public_id = Blog.objects.filter(public=False).values_list("id",flat=True)
        blocks =Blocks.objects.filter(header__contains=word,title__contains=word).exclude(id__in=not_public_id)
        block_serializer = BlocksSerializer(blocks,many=True)
        
        obj = GetObjects(users,blogs)
        return Response({
            "user":request.user.username,
            "id__":request.user.id,
            "data":{
                "users":obj['users'],
                "blogs":obj['blogs'],
                "blocks":block_serializer.data
            }
        })
