from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import Blocks,Blog,BlocksSerializer,BlogSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class CreateBlog(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request=Request):
        data = {
            "author":request.user.id,
            "header":request.data["header"],
            "image":request.data['image']
        }
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def get(self,request:Request):
        private_blogs = Blog.objects.filter(public=False,author=request.user)
        serializer = BlogSerializer(private_blogs,many=True)
        return Response(serializer.data)