from django.urls import path
from .views import RecommendedBlogs,RecommendByAuthor

# to app News
urlpatterns = [
    path("perconal1/",RecommendedBlogs.as_view()),
    path("perconal2/",RecommendByAuthor.as_view())
]
