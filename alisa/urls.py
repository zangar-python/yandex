from django.urls import path
from .views import alisaSetCommand

urlpatterns = [
    path("",alisaSetCommand.as_view())
]
