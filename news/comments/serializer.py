from news.models import Comment
from rest_framework.serializers import ModelSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"