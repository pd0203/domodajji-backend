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
            user = User.objects.get(id=user_id)
            request.user = user
        except jwt.exceptions.DecodeError as d:
            return Response({'ERROR_MESSAGE': d.args}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist as n:
            return Response({'ERROR_MESSAGE': n.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'ERROR_MESSAGE': e.args}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, *args, **kwargs)
    return wrapper