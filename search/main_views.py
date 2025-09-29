from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

# from search.parsing.parse import get_data_from_redis

class GetData(APIView):
    permission_classes = [IsAuthenticated]
    def get(seld,request:Request):
        data = {
            "user":request.user.username,
            "id":request.user.id,
            # "data":get_data_from_redis.delay().get()
        }
        return Response(data=data)