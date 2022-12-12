from users.models import User 
from users.serializers import * 
from utils.token import generate_access_token
from utils.token import generate_refresh_token
from utils.token import generate_access_token_by_refresh_token
from rest_framework import status 
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response 

class UserSignUpAPI(generics.CreateAPIView): 
      serializer_class = UserSignUpSerializer
      def create(self, request, *args, **kwargs):
          try:
            instance = self.get_serializer(data=request.data)
            instance.is_valid(raise_exception=True)
            instance.save()
            user_email = instance.data['email']
            access_token = generate_access_token(user_email)
            refresh_token = generate_refresh_token(user_email) 
            token_set = {
                'access_token': access_token, 
                'refresh_token': refresh_token
            } 
            return Response(token_set, status=status.HTTP_201_CREATED)
          except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 

# class UserLoginAPI(generics.CreateAPIView):
