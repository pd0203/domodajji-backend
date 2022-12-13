from users.models import User 
from users.serializers import * 
from utils.token import generate_token_set 
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
            token_set = generate_token_set(user_email) 
            return Response(token_set, status=status.HTTP_201_CREATED)
          except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 

class UserLoginAPI(generics.CreateAPIView):
      serializer_class = UserLoginSerializer
      def create(self, request, *args, **kwargs):
          try:
            instance = self.get_serializer(data=request.data)
            instance.is_valid(raise_exception=True)
            user_email = instance.data['email']
            token_set = generate_token_set(user_email) 
            return Response(token_set, status=status.HTTP_200_OK)
          except NotFound as n:
            return Response({'ERROR_MESSAGE': n.args}, status=status.HTTP_404_NOT_FOUND)
          except ValidationError as v:
            return Response({'ERROR_MESSAGE': v.args}, status=status.HTTP_400_BAD_REQUEST)
          except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 