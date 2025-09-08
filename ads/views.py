from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import Ad
from .serializers import AdSerializer


class GetSetAd(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request):
        user:User = request.user
        obj = {
            "img":request.data.get("img"),
            "header":request.data.get("header"),
            "text":request.data.get("text"),
            "to_link":request.data.get("to_link"),
            "author":user.pk
        }
        serilizer = AdSerializer(data=obj)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors)
    def get(self,request:Request):
        my_ads = Ad.objects.filter(author=request.user.id)
        serializer = AdSerializer(my_ads,many=True)
        return Response(serializer.data)