from django.urls import path, include
from users.views import UserSignUpAPI

urlpatterns = [
    path('signup', UserSignUpAPI.as_view(), name='signup'),
]