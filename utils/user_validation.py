from users.models import User
from utils.token import verify_token
from rest_framework import status
from rest_framework.response import Response

import jwt

# DRF permission으로 대체 가능
def user_validator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization', None).split()[1]
            user_id = verify_token(token)
            is_user = User.objects.filter(id=user_id).exists()
            if is_user is False:
               raise Exception('User is not registered')
            request.user_id = user_id
        except jwt.exceptions.DecodeError as d:
            return Response({'ERROR_MESSAGE': d.args}, status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError as a:
           return Response({'ERROR_MESSAGE': {'Access token is not provided'}}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
           return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, *args, **kwargs)
    return wrapper