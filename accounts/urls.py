from django.urls import path
from .views import UserRegisterView,UserLoginView,UserProfile,UserLikedBlogs,UserFollowing,UserFollowers,UserFollowings

urlpatterns = [
    path("register/",UserRegisterView.as_view()),
    path("login/",UserLoginView.as_view()),
    path('profile/',UserProfile.as_view()),
    path('profile/liked_blogs/',UserLikedBlogs.as_view()),
    path('follow/<int:pk>/',UserFollowing.as_view()),
    path('followings/',UserFollowings.as_view()),
    path('followers/',UserFollowers.as_view())
]