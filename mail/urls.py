from django.urls import path
from .views import MessageRead,NewMessages,AllMessages

urlpatterns = [
    path('message/new/',NewMessages.as_view()),
    path('message/<int:pk>/',MessageRead.as_view()),
    path('message/',AllMessages.as_view())
]
