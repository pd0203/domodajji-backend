from django.urls import path, include
from users.views import UserSignUpAPI, UserLoginAPI 

urlpatterns = [
    path('signup', UserSignUpAPI.as_view(), name='signup'),
    path('login', UserLoginAPI.as_view(), name='login'),
]