from django.urls import path
from .views import FileGetPostViews,FileDeleteGet

urlpatterns = [
    path("",FileGetPostViews.as_view()),
    path("<int:pk>/",FileDeleteGet.as_view())
]
