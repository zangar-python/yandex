# Еще в ходе разработки

from rest_framework.response import Response
from rest_framework.request import Request

from news.serializers import Blog,BlogSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

class RecommendedBlogs(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request):
        user = request.user
        liked_blogs = user.liked_blogs.all()
        
        if not liked_blogs.exists():
            return Response(data={"data":"У вас нету лайков.Так что рекомендаций тоже нет."})
        
        similar_users = User.objects.filter(
            liked_blogs__in=liked_blogs
        ).exclude(
            id = user.id
        ).annotate(
            same_likes = Count("liked_blogs")
        ).order_by("-liked_blogs")
        
        user_liked_blogs_id = liked_blogs.values_list("id",flat=True)
        
        recommended_blogs = Blog.objects.filter(
            likes__in = similar_users
        ).exclude(
            id__in=user_liked_blogs_id
        ).distinct().annotate(
            sum_likes = Count("likes")
        ).order_by("-sum_likes")[:10]
        
        serilizer = BlogSerializer(recommended_blogs,many=True)
        return Response(serilizer.data)
        
class RecommendByAuthor(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request):
        user = request.user
        user_liked_blogs = user.liked_blogs.all()
        
        authors_this_blogs = User.objects.filter(
            blogs__in=user_liked_blogs
        ).exclude(
            id=user.id
        ).distinct()
        
        user_liked_blogs_id = user_liked_blogs.values_list("id",flat=True)
        
        recommend = Blog.objects.filter(
            author__in=authors_this_blogs
        ).exclude(
            id__in=user_liked_blogs_id
        ).distinct().annotate(
            sum_likes = Count("likes")
        ).order_by("-sum_likes")[:10] 
        
        serializer = BlogSerializer(recommend,many=True)
        return Response(serializer.data)