from ads.models import Ad
from ads.serializers import AdSerializer


def itSerialized(data):
    serializer = AdSerializer(data,many=True)
    return serializer.data
    
def defaultRecommends():
    return itSerialized(Ad.objects.all().order_by("-created_at")[:10])