from ads.models import Ad
from ads.serializers import AdSerializer
from search.models import Story
from django.contrib.auth.models import User

def itSerialized(data):
    serializer = AdSerializer(data,many=True)
    return serializer.data
    
def defaultRecommends():
    return itSerialized(Ad.objects.all().order_by("-created_at")[:10])

# def byStory(user):
#     story = user.story.all().values_list("text",flat=True)
    
#     ad = Ad.objects.filter(
#         header__in__contains=story,
#         text__in__contains=story
#     ).order_by("-created_at")[:10]
#     return itSerialized(ad)


def recommendByStory(user:User):
    storys = Story.objects.filter(user=user).order_by("-created_at").values_list("text",flat=True)
    recomends = []
    for  story in storys:
        ad = Ad.objects.filter(
            header__contains=story
        ).order_by("-created_at").first()
        if ad:
            if not ad in recomends:    
                recomends.append(ad)
                
    return {
        "by_story":itSerialized(recomends),
        "default":defaultRecommends()
    }
    
    