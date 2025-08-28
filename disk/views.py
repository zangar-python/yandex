from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializer import FileSerializer,File

class FileGetPostViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request):
        user = request.user
        obj = {
            "user":user.id,
            "title":request.data.get("title"),
            "file":request.data.get("file")
        }
        serializer = FileSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"details":"saved!","data":serializer.data},status=status.HTTP_200_OK)
        return Response(data={"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request:Request):
        user = request.user
        user_files = File.objects.filter(
            user=user
        ).order_by(
            "-created_at"
        )
        serializer = FileSerializer(user_files,many=True)
        return Response(data={
            "username":user.username,
            "saved_files":serializer.data
        })