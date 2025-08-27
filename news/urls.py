from django.urls import path,include
from .views import CreateBlog,CreateBlocks,BlogGet,BlogSetPublic,BlogLiked,BlogsGetList

urlpatterns = [
    path("private/",CreateBlog.as_view()),
    path("<int:pk>/",BlogGet.as_view()),
    path("<int:pk>/blocks/",CreateBlocks.as_view()),
    path("<int:pk>/set_public/",BlogSetPublic.as_view()),
    path("<int:pk>/like/",BlogLiked.as_view()),
    path("recommend/",include("recommend.urls")),
    path("",BlogsGetList.as_view())
]

