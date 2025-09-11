from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .commands import AlisaMethods

class alisaSetCommand(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request:Request):
        user = request.user
        alisa = AlisaMethods(user)
        data = alisa.command(request.data.get("command"))
        print(request.data.get('command'))
        return Response(data={
            "results":data
        })