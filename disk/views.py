from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializer import FileSerializer,File
import os
from django.http import FileResponse

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

class FileDeleteGet(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request,pk):
        file = get_object_or_404(File,pk=pk)
        # serilizer = FileSerializer(file)
        # return Response(data={
        #     "user":request.user.username,
        #     "data":serilizer.data
        # })
        if not file.user == request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_path = file.file.path
        if not os.path.exists(file_path):
            return Response(status=status.HTTP_404_NOT_FOUND,data={"detail":"Файл отсуствует"})
        return FileResponse(open(file_path,"rb"),as_attachment=True,filename=file.title)
        
    def delete(self,request:Request,pk):
        user = request.user
        file = get_object_or_404(File,pk=pk)
        if not file.user == user:
            return Response(data={"detail":"У вас нет доступа"},status=status.HTTP_403_FORBIDDEN)
        file.delete()
        return Response(data={
            "detail":"deleted"
        })