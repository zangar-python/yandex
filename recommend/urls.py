from django.urls import path
from .views import RecommendedBlogs,RecommendByAuthor,ReccomendFollowings

# to app News
urlpatterns = [
    path("p1/",RecommendedBlogs.as_view()),
    path("p2/",RecommendByAuthor.as_view()),
    path("p3/",ReccomendFollowings.as_view()),
]
