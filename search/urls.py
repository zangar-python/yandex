from django.urls import path
from .views import FilterGet

urlpatterns = [
    path("<str:word>/",FilterGet.as_view())
]
