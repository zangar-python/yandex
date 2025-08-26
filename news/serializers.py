from .models import Blog,Blocks
from rest_framework.serializers import ModelSerializer

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class BlocksSerializer(ModelSerializer):
    class Meta:
        model = Blocks
        fields = "__all__"
