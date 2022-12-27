from django.urls import path, include
from users.views import UserSignUpAPI, UserLoginAPI, UserInfoAPI 

urlpatterns = [
    path('signup', UserSignUpAPI.as_view(), name='signup'),
    path('login', UserLoginAPI.as_view(), name='login'),
    path('user-info', UserInfoAPI.as_view({'patch': 'partial_update'}), name='user_info'),
]