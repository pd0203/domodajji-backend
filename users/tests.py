import json
from django.urls import reverse 
from rest_framework.test import APITestCase
from django.test import override_settings

# # TestCase 작성시 Rules
# # 1. 하나의 API에 대해 성공 케이스와 실패 케이스 모두 작성
# # 2. 성공 케이스 & 실패 케이스 각 1개씩 작성  
# # 3. test 파일의 이름은 test로 시작
# # 4. test 파일내 test 함수명은 test로 시작 

class UserTest(APITestCase): 
    @override_settings(DEBUG=True)
    def test_signup_success(self): 
        url = reverse("signup")
        user_data = {
          "name": "Hyosang Park",
          "email": "adefg@gmail.com",
          "password1": "abde1235",
          "password2": "abde1235",
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 201)
    @override_settings(DEBUG=True)        
    def test_signup_failure(self): 
        url = reverse("signup")
        user_data = {
          "name": "April",
          "email": "abcd@gmail.com",
          "password1": "abcd1235",
          "password2": "abcd1235",
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)

    # def test_user_list(self):
    #   # make a GET request to the user list endpoint
    #   response = self.client.get('/users/')
  
    #   # assert that the response has a 200 status code (success)
    #   self.assertEqual(response.status_code, 200)
  
    #   # assert that the response data includes the expected number of users
    #   self.assertEqual(len(response.data), 10)
  
    #   # assert that the response data includes the expected user data
    #   for user in response.data:
    #     self.assertIn('id', user)
    #     self.assertIn('username', user)
    #     self.assertIn('email', user)