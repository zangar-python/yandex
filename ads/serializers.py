from .models import Ad
from rest_framework.serializers import ModelSerializer

class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"