from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import Message,MessageSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class NewMessages(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request:Request):
        messages = Message.objects.filter(to_user=request.user,is_readed=False)
        serializer = MessageSerializer(messages,many=True)
        count = messages.count()
        return Response({
            "count":count,
            "messages":serializer.data
        })
    def post(self,request:Request):
        header = request.data['header']
        text = request.data['text']
        to_user = request.data['to_user']
        from_user = request.user.id
        data = {
            "header":header,
            "text":text,
            "to_user":to_user,
            "from_user":from_user
        }
        
        serilizer = MessageSerializer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response("sended!")
        return Response(serilizer.errors,status.HTTP_400_BAD_REQUEST)

class MessageRead(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request:Request,pk):
        message = get_object_or_404(Message,pk=pk)
        message.is_readed = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    
class AllMessages(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request:Request):
        messages = Message.objects.filter(to_user=request.user)
        serilizer = MessageSerializer(messages,many=True)
        return Response(serilizer.data)
