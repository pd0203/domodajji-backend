import jwt
import datetime
from rest_framework import status 
from django.conf import settings

# Secret Key
secret_key = getattr(settings, 'SECRET_KEY')

# Hashing Algorithm
hashing_algorithm = 'HS512'

# Token Expiration Period
access_token_expiration_period = datetime.timedelta(hours=3)
refresh_token_expiration_period = datetime.timedelta(days=7)

def generate_access_token(email):
    current_datetime = datetime.datetime.utcnow()
    access_token_payload = {
        'exp': current_datetime + access_token_expiration_period, 
        'email': email
    }
    access_token = jwt.encode(access_token_payload, secret_key, hashing_algorithm) 
    return access_token 

def generate_refresh_token(email):
    current_datetime = datetime.datetime.utcnow()
    refresh_token_payload = {
        'exp': current_datetime + refresh_token_expiration_period, 
        'email': email
    }
    refresh_token = jwt.encode(refresh_token_payload, secret_key, hashing_algorithm)
    return refresh_token 

def generate_token_set(email):
    access_token = generate_access_token(email)
    refresh_token = generate_refresh_token(email)
    token_set = {
      'access_token': access_token,
      'refresh_token': refresh_token
    }
    return token_set 
    
def generate_access_token_by_refresh_token(refresh_token): 
    try: 
      current_datetime = datetime.datetime.utcnow()
      refresh_token_payload = jwt.decode(refresh_token, secret_key, hashing_algorithm)
      user_email = refresh_token_payload['email']
      access_token = generate_access_token(user_email)
      return access_token 
    except jwt.InvalidTokenError: 
      return status.HTTP_401_UNAUTHORIZED
    
def verify_token(access_token):
    try: 
      jwt.decode(access_token, secret_key, hashing_algorithm)
    # signature가 맞지 않거나 유효시간이 지난 토큰 에러 
    except jwt.InvalidTokenError: 
      return status.HTTP_401_UNAUTHORIZED
    return True 