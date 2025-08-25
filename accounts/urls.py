from django.urls import path
from .views import UserRegisterView,UserLoginView,UserProfile

urlpatterns = [
    path("register/",UserRegisterView.as_view()),
    path("login/",UserLoginView.as_view()),
    path('profile/',UserProfile.as_view())
]