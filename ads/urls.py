from django.urls import path
from .views import GetSetAd

urlpatterns = [
    path("",GetSetAd.as_view())
]
