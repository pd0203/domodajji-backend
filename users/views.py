from users.models import User 
from users.serializers import UserSignUpSerializer, UserLoginSerializer, UserUpdateSerializer
from utils.token import generate_token_set 
from utils.user_validation import user_validator 
from utils.s3 import S3Client
from rest_framework import status 
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound
from django.db import transaction 
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import Http404

# AWS S3 
AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = getattr(settings, 'AWS_S3_BUCKET_NAME')

class UserSignUpAPI(generics.CreateAPIView): 
      serializer_class = UserSignUpSerializer
      @transaction.atomic
      def create(self, request, *args, **kwargs):
          try:
            instance = self.get_serializer(data=request.data)
            instance.is_valid(raise_exception=True)
            instance.save()
            user_id = instance.data['id']
            token_set = generate_token_set(user_id) 
            return Response(token_set, status=status.HTTP_201_CREATED)
          except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 

class UserLoginAPI(generics.CreateAPIView):
      serializer_class = UserLoginSerializer
      @transaction.atomic
      def create(self, request, *args, **kwargs):
          try:
            instance = self.get_serializer(data=request.data)
            instance.is_valid(raise_exception=True)
            instance.save()
            user_id = instance.data['id']
            token_set = generate_token_set(user_id) 
            return Response(token_set, status=status.HTTP_200_OK)
          except NotFound as n:
            return Response({'ERROR_MESSAGE': n.args}, status=status.HTTP_404_NOT_FOUND)
          except Exception as e:
            return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 

class UserInfoAPI(ModelViewSet):
    queryset = User.objects.all()  
    s3_client = S3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME)
    def get_object(self): 
        queryset = self.get_queryset()
        if self.action == 'partial_update':
           return get_object_or_404(queryset, id=self.request.user.id)
        return get_object_or_404(self.get_queryset()) 
    def get_serializer_class(self):
        if self.action == 'partial_update':
           return UserUpdateSerializer
    @transaction.atomic 
    @user_validator
    def partial_update(self, request, *args, **kwargs):
        try: 
          user_instance = self.get_object()
          json_data = self.formdata_to_json(request)
          serializer = self.get_serializer(user_instance, data=json_data, partial=True)
          serializer.is_valid(raise_exception=True)
          self.perform_update(serializer)
          if getattr(user_instance, '_prefetched_objects_cache', None):
             user_instance._prefetched_objects_cache = {}
          return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as n:
            return Response({'ERROR_MESSAGE': n.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST) 
    def formdata_to_json(self, request): 
        form_data = request.data
        profile_image_file = request.FILES.get('profile_image')
        json_data = {
            'profile_img_url': self.s3_client.upload(profile_image_file),
            'birthday': form_data['birthday'],
            'phone_number': form_data['phone_number']
        }
        return json_data
