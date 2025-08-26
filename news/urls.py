from django.urls import path
from .views import CreateBlog,CreateBlocks,BlogGet

urlpatterns = [
    path("private/",CreateBlog.as_view()),
    path("<int:pk>/",BlogGet.as_view()),
    path("<int:pk>/blocks/",CreateBlocks.as_view())
]
