from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import Blocks,Blog,BlocksSerializer,BlogSerializer
from django.shortcuts import get_object_or_404


