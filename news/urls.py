from django.urls import path
from .views import CreateBlog

urlpatterns = [
    path("private/",CreateBlog.as_view())
]
