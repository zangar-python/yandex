from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import Blocks,Blog,BlocksSerializer,BlogSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class CreateBlog(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request):
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

class CreateBlocks(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request,pk):
        blog = get_object_or_404(Blog,pk=pk)
        if blog.author != request.user:
            return Response("У вас нет доступа к этому блогу")
        if blog.public == True:
            return Response("Он уже опубликован.Ее нельзя изменить")
        
        data = {
            "header":request.data['header'],
            "title":request.data['title'],
            "image":request.data['image'],
            "blog":blog.id
        }
        serializer = BlocksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Created!")
        return Response(serializer.errors)
        # return Response("Test")
class BlogGet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request:Request,pk):
        blog = get_object_or_404(Blog,pk=pk)
        if blog.public == False:
            if blog.author != request.user:
                return Response(data={"Доступ запрещен"})
        blocks = blog.blocks.all()
        blog_serializer = BlogSerializer(blog)
        blocks_serializer = BlocksSerializer(blocks,many=True)
        return Response(
            {
                "Blog":blog_serializer.data,
                "Blocks":blocks_serializer.data
            }
        )
    
        
         