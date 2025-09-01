from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializer import Comment,CommentSerializer
from news.models import Blog

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from mail.messages import send_comment,send_comment_like

class GetSetComments(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request,pk:int):
        blog : Blog = get_object_or_404(Blog,pk=pk)
        if not blog.public:
            return Response(data={"detail":"blog is not public"})
        user : User = request.user
        obj = {
            "to_blog":blog.id,
            "user":user.id,
            "text":request.data.get("text")
        }
        # comment = Comment.objects.create(
        #     to_blog=blog,
        #     user=user,
        #     text=request.data.get("text")
        # )
        
        serializer = CommentSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            send_comment(serializer.data.id)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get(self,request:Request,pk):
        blog = get_object_or_404(Blog,pk=pk)
        comments = Comment.objects.filter(to_blog=blog).annotate(count_likes = Count("likes")).order_by("-count_likes")
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)

class LikeComment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request,pk):
        comment = get_object_or_404(Comment,pk=pk)
        user : User = request.user
        
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response(data={
                "detail":"like is deleted",
                "user":user.username,
                "to_comment":comment.text
            })
        if not user in comment.likes.all():
            comment.likes.add(user)
            send_comment_like(comment,user)
            return Response(data={
                "detail":"like is added",
                "user":user.username,
                "to_comment":comment.text
            })
        else:
            return Response({"err":"Error..."})
        